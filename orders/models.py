from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signals import request_finished
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField

user = get_user_model()

SM = 'Small'
LG = 'Large'

SIZE_CHOICE = [
        (SM, 'Small'),
        (LG, 'Large'),
    ]

class Customer(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'
        
class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from='name', default=0)

    def __str__(self):
        return f'{self.name}'

class MenuItem(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_large = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def is_valid_price(self):
        if self.price_large:
            return (self.price_large > self.price) and (self.price > 0)
        else:
            return (self.price > 0)

class Topping(models.Model):
    name = models.CharField(max_length=64)
    is_topping_subs = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    customer = models.ForeignKey(user, on_delete=models.CASCADE, related_name='orders')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateField(auto_now=True)
    CART = 'CT'
    PROCESSING = 'PR'
    DONE = 'DN'
    ORDER_STATES_CHOICES = [
        (CART, 'cart'),
        (PROCESSING, 'processing'),
        (DONE, 'done'),
    ]
    order_state = models.CharField(
        max_length=2,
        choices=ORDER_STATES_CHOICES,
        default=CART,
    )
    final_price = models.DecimalField(max_digits=6, decimal_places=2)

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.pk})

    def get_price(self):
        price = 0
        for item in self.items.all():
            price += float(item.get_price)
        return price

    def save(self, *args, **kwargs):
        self.final_price = self.get_price()
        super(Order, self).save(*args, **kwargs)
        
    def is_valid_price(self):
        return self.final_price > 0 

    def __str__(self):
        return f'{self.id} {self.customer_id} ({self.time_created})'

class MenuInstance(models.Model):
    customer = models.ForeignKey(user, on_delete=models.CASCADE)
    kind = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True)
    n_items = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICE,
        default=SM,
    )
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='items')

    # Calling this get price to update the order price, when subs I need to count the toppings, 
    # so I skip the counting when instance created and calculate on M2M changed in signal
    @property
    def get_price(self):
        price = 0
        if self.size == SM:
            price = self.kind.price * self.n_items
        elif self.size == LG:
            price = self.kind.price_large * self.n_items
        if self.kind.category.name == 'Subs':
            if not self.pk: 
                pass
            else:
                price = float(price) + self.toppings.all().count() * 0.50
        return price

    def is_valid_price(self):
        return self.get_price > 0   

    def __str__(self):
        return f'{self.kind}'






