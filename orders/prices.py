from .models import Pizza, Sub, Dinner, Order

def price_pizza(Pizza):

    if Pizza.size.size == 'SM' and Pizza.is_sicilian == False:
        return Pizza.pizza_type.price_regular
    elif Pizza.size.size == 'SM' and Pizza.is_sicilian == True:
        return Pizza.pizza_type.price_sicilian
    elif Pizza.size.size == 'LG' and Pizza.is_sicilian == False:
        return Pizza.pizza_type.price_large
    elif Pizza.size.size == 'LG' and Pizza.is_sicilian == True:
        return Pizza.pizza_type.price_sicilian_large
    else:
        return -1

def price_sub(Sub):
    if Sub.size.size == 'SM':
        return Sub.sub_type.price
    elif Sub.size.size == 'LG':
        return Sub.sub_type.price_large
    else:
        return -1

def price_dinner(Dinner):
    if Dinner.size.size == 'SM':
        return Dinner.dinner_type.price
    elif Dinner.size.size == 'LG':
        return Sub.dinner_type.price_large
    else:
        return -1

def price_order(Order):
    price_pizzas = 0
    price_subs = 0
    price_dinners = 0
    price_salads = 0
    price_pastas = 0
    for pizza in Order.item_pizza.all():
        price_pizzas = price_pizzas + pizza.final_price
    for sub in Order.item_subs.all():
        price_subs += sub.final_price
    for dinner in Order.item_dinner.all():
        price_dinners += dinner.final_price
    for pasta in Order.item_pasta.all():
        price_pastas += pasta.final_price
    for salad in Order.item_salad.all():
        price_salads += salad.final_price

    return price_pizzas + price_subs + price_dinners + price_salads + price_pastas






