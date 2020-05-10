from .models import Order

def cart(request):
    cart = False
    try:
        order = Order.objects.get(customer=request.user.pk, is_confirmed=False)
        n_items = order.items.count()
        cart = True
    except Order.DoesNotExist:
        cart = False 
        n_items = 0
        order = None
    return {'cart': n_items, 'order': order}
        