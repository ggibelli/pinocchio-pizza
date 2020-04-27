from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Category, Customer , MenuInstance, Order, MenuItem, Topping


class DishesChoicesTest(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'prova',
            email = 'prova@prova.it',
            password = 'prova123'
        )
        customer = Customer.objects.get(user = user)
        category = Category.objects.create(name='buono')
        category2 = Category.objects.create(name='cattivo')

        pizza = MenuItem.objects.create(
            name = 'bbb',
            category=category,
            price = 5.0,
            price_large = 10.0
        )
        sub = MenuItem.objects.create(
            name = 'ccc',
            category=category2,
            price = 20.0,
            price_large = 25.0
        )

        tops1 = Topping.objects.create(name='abc')
        tops2 = Topping.objects.create(name='bac')
        tops3 = Topping.objects.create(name='cab')
        pizza = MenuInstance.objects.create(
            customer = user,
            kind = pizza,
            size = 'Small',
            n_items = 1,
            #final_price = 5
        )
        pizza.toppings.add(tops1, tops2)
        sub = MenuInstance.objects.create(
            customer = user,
            kind = sub,
            size = 'Large',
            n_items = 2,
            #final_price = 50
        )
        sub.toppings.add(tops3)
        

    def test_dishes_count(self):
        self.assertEqual(MenuItem.objects.count(), 2)

    def test_is_valid_menu(self):
        sub = MenuItem.objects.get(name='bbb')
        self.assertTrue(sub.is_valid_price())

    def test_is_valid_instance(self):
        pizza = MenuInstance.objects.all()[0]
        self.assertTrue(pizza.is_valid_price())

    def test_pizza_ntoppings(self):
        kind = MenuItem.objects.get(name='bbb')
        pizza = MenuInstance.objects.get(kind=kind)
        self.assertEqual(pizza.toppings.count(), 2)

    def test_order_right_state(self):
        order = Order.objects.all()[0]
        self.assertEqual(order.order_state, 'CT')

    def test_order_right_price(self):
        order = Order.objects.all()[0]
        self.assertEqual(order.final_price, order.get_price())
        self.assertTrue(order.is_valid_price())

    def test_order_user(self):
        order = Order.objects.all()[0]
        user = Customer.objects.all()[0]
        self.assertEqual(order.customer_id, user.id)

    def test_order_user_count(self):
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.orders.count(), 1)

    def test_items_count(self):
        order = Order.objects.all()[0]
        self.assertEqual(order.items.count(), 2)






