from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import MenuInstance, Order


user = get_user_model()


# When the MenuInstance is created I add it to the order in cart state, if no orders in CT state
# I create a new order instance, and I set the price calling the get_price method
@receiver(post_save, sender=MenuInstance)
def create_order_item(sender, instance, created, **kwargs):
    if created:
        try:
            order = Order.objects.get(customer=instance.customer, is_confirmed=False)
        except:
            order = Order.objects.create(customer=instance.customer, final_price=instance.price)
        order.items.add(instance)
        order.final_price = order.get_price()
        order.save()
    else:
        update_order(instance)

@receiver(post_delete, sender=MenuInstance)
def delete_order_item(sender, instance, **kwargs):
    try:
        order = Order.objects.get(customer=instance.customer, is_confirmed=False)
        order.final_price = order.get_price()
        
    except Order.DoesNotExist:
        return

@receiver(post_save, sender=Order)
def order_ready(sender, instance, **kwargs):
    if instance.order_state == 'Done':
        subject = f'The order n. {instance.id} is ready'
        message = f'You can pick up now your items'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.customer.email,]
        send_mail( subject, message, email_from, recipient_list )

# If the menuinstance is a topping I need to calculate the price counting the toppings (m2m) so I need to wait
# for this signal, then I call the get_price method
@receiver(m2m_changed, sender=MenuInstance.toppings.through)
def sub_price_order(sender, instance, **kwargs):
    update_order(instance)


def update_order(instance):
    order = Order.objects.get(customer=instance.customer, is_confirmed=False)
    order.final_price = order.get_price()
    order.save()
    

        
        