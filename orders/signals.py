from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .models import Customer, MenuInstance, Order


user = get_user_model()

@receiver(post_save, sender=user)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

# When the MenuInstance is created I add it to the order in cart state, if no orders in CT state
# I create a new order instance, and I set the price calling the get_price method
@receiver(post_save, sender=MenuInstance)
def create_order_item(sender, instance, created, **kwargs):
    if created:
        try:
            order = Order.objects.get(customer=instance.customer, order_state='CT')
        except:
            order = Order.objects.create(customer=instance.customer, final_price=instance.get_price)
        order.items.add(instance)
        order.final_price = order.get_price()
        order.save()
    else:
        order = Order.objects.get(customer=instance.customer, order_state='CT')
        order.final_price = order.get_price()
        order.save()

@receiver(post_delete, sender=MenuInstance)
def delete_order_item(sender, instance, **kwargs):
    try:
        order = Order.objects.get(customer=instance.customer, order_state='CT')
        order.final_price = order.get_price()
        order.save()
    except Order.DoesNotExist:
        return

# If the menuinstance is a topping I need to calculate the price counting the toppings (m2m) so I need to wait
# for this signal, then I call the get_price method
@receiver(m2m_changed, sender=MenuInstance.toppings.through)
def sub_price_order(sender, instance, **kwargs):
    order = Order.objects.get(customer=instance.customer, order_state='CT')
    order.final_price = order.get_price()
    order.save()
    

        
        