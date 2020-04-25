from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer, MenuInstance, Order

user = get_user_model()


@receiver(post_save, sender=user)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=MenuInstance)
def create_order_item(sender, instance, created, **kwargs):
    if created:
        try:
            order = Order.objects.get(customer=instance.customer, order_state='CT')
        except:
            order = Order.objects.create(customer=instance.customer, final_price=instance.get_price())
        order.items.add(instance)
        order.final_price = order.get_price()
        order.save()
        
        