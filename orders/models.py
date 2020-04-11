from django.db import models
from django.conf import settings


class Size(models.Model):
    SMALL = 'SM'
    LARGE = 'LG'
    SIZE_CHOICE = [
        (SMALL, 'Small'),
        (LARGE, 'Large'),
    ]
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICE,
        default=SMALL,
    )
    
    def __str__(self):
        return f'{self.size}'

class PizzaChoice(models.Model):
    name = models.CharField(max_length=64)
    price_regular = models.DecimalField(max_digits=6, decimal_places=2)
    price_sicilian = models.DecimalField(max_digits=6, decimal_places=2)
    price_large = models.DecimalField(max_digits=6, decimal_places=2)
    price_sicilian_large = models.DecimalField(max_digits=6, decimal_places=2)

    def is_valid_price(self):
        return (self.price_sicilian_large > self.price_sicilian) and (self.price_large > self.price_regular) and self.price_regular > 0.0

    def __str__(self):
        return f'{self.name}'

class SubChoice(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_large = models.DecimalField(max_digits=6, decimal_places=2)

    def is_valid_price(self):
        return (self.price_large > self.price) and (self.price > 0)

    def __str__(self):
        return f'{self.name}'

class DinnerChoice(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_large = models.DecimalField(max_digits=6, decimal_places=2)

    def is_valid_price(self):
        return (self.price_large > self.price) and (self.price > 0)

    def __str__(self):
        return f'{self.name}'

class Pizza(models.Model):
    pizza_type = models.ForeignKey(PizzaChoice, on_delete=models.CASCADE)
    is_sicilian = models.BooleanField(default=False)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=6, decimal_places=2, null=True) 

    def is_valid_price(self):
        return self.final_price > 0       

    def __str__(self):
        return f'{self.pizza_type} {self.is_sicilian} {self.size}'

class Sub(models.Model):
    sub_type = models.ForeignKey(SubChoice, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def is_valid_price(self):
        return self.final_price > 0 

    def __str__(self):
        return f'{self.sub_type} {self.size}'

class Topping(models.Model):
    name = models.CharField(max_length=64)
    is_topping_subs = models.BooleanField(default=False)
    pizzas = models.ManyToManyField(Pizza, blank=True, related_name='toppings')
    subs = models.ManyToManyField(Sub, blank=True, related_name='toppings')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.name} {self.is_topping_subs}'

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    final_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name}'

class Salad(models.Model):
    name = models.CharField(max_length=64)
    final_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name}'
    
class Dinner(models.Model):
    dinner_type = models.ForeignKey(DinnerChoice, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def is_valid_price(self):
        return self.final_price > 0 

    def __str__(self):
        return f'{self.dinner_type} {self.size}'

class Order(models.Model):
    item_pizza = models.ManyToManyField(Pizza, blank=True)
    item_subs = models.ManyToManyField(Sub, blank=True)
    item_salad = models.ManyToManyField(Salad, blank=True)
    item_pasta = models.ManyToManyField(Pasta, blank=True)
    item_dinner = models.ManyToManyField(Dinner, blank=True)
    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='orders')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateField(auto_now=True)
    RECEIVED = 'RC'
    PROCESSING = 'PR'
    DONE = 'DN'
    ORDER_STATES_CHOICES = [
        (RECEIVED, 'received'),
        (PROCESSING, 'processing'),
        (DONE, 'done'),
    ]
    order_state = models.CharField(
        max_length=2,
        choices=ORDER_STATES_CHOICES,
        default=RECEIVED,
    )
    final_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def is_valid_price(self):
        return self.final_price > 0 

    def __str__(self):
        return f'{self.id} {self.customer_id} ({self.time_created})'

