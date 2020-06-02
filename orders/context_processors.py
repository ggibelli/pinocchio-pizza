from .models import Order, Category

def cart(request):
    try:
        categories = Category.objects.all()
        order = Order.objects.get(customer=request.user.pk, is_confirmed=False)
        n_items = order.items.count()
        cart = True
    except Order.DoesNotExist:
        cart = False 
        n_items = 0
        order = None
    except Category.DoesNotExist:
        categories = None
    return {'cart': n_items, 'order': order, 'categories': categories}
        