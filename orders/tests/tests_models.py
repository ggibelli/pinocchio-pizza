from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from orders.models import Category, MenuInstance, Order, MenuItem, Topping


class OrdersModelsTest(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'prova',
            email = 'prova@prova.it',
            password = 'prova123'
        )
        category = Category.objects.create(name='Subs')
        category2 = Category.objects.create(name='Dinners')
        category3 = Category.objects.create(name='Salad')
        category4 = Category.objects.create(name='Salad')
        item_sub = MenuItem.objects.create(
            name = 'sub',
            category=category,
            price = 5.0,
            price_large = 10.0
        )
        item_dinner = MenuItem.objects.create(
            name = 'dinner',
            category=category2,
            price = 20.0,
            price_large = 25.0
        )

        item_salad = MenuItem.objects.create(
            name = 'salad',
            category=category3,
            price = 20.0,
        )

        item_pizza = MenuItem.objects.create(
            name = 'pizza',
            category=category4,
            price = 20.0,
            price_large = 25.0
        )
        tops1 = Topping.objects.create(name='abc')
        tops2 = Topping.objects.create(name='bac')
        tops3 = Topping.objects.create(name='cab')
        pizza = MenuInstance.objects.create(
            customer = user,
            kind = item_pizza,
            size = 'Small',
            n_items = 1,
        )
        pizza.toppings.add(tops1, tops2)
        sub = MenuInstance.objects.create(
            customer = user,
            kind = item_sub,
            size = 'Large',
            n_items = 2,
        )
        sub.toppings.add(tops3)
        pizza.n_items = 2
        pizza.save()
        

    def test_dishes_count(self):
        self.assertEqual(MenuItem.objects.count(), 4)

    def test_is_valid_menu(self):
        sub = MenuItem.objects.get(name='sub')
        self.assertTrue(sub.is_valid_price())

    def test_is_valid_instance(self):
        pizza = MenuInstance.objects.all()[0]
        self.assertTrue(pizza.is_valid_price())

    def test_pizza_ntoppings(self):
        kind = MenuItem.objects.get(name='pizza')
        pizza = MenuInstance.objects.get(kind=kind)
        self.assertEqual(pizza.toppings.count(), 2)

    def test_order_cart_state(self):
        order = Order.objects.all()[0]
        self.assertFalse(order.is_confirmed)
        self.assertEqual(order.order_state, 'Cart')

    def test_order_confirmed_state(self):
        order = Order.objects.all()[0]
        order.is_confirmed = True
        order.save()
        self.assertEqual(order.order_state, 'Processing')

    def test_order_right_price(self):
        order = Order.objects.all()[0]
        self.assertEqual(order.final_price, order.get_price())
        self.assertTrue(order.is_valid_price())

    def test_order_user(self):
        order = Order.objects.all()[0]
        user = get_user_model().objects.all()[0]
        self.assertEqual(order.customer_id, user.id)

    def test_order_user_count(self):
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.orders.count(), 1)

    def test_items_count(self):
        order = Order.objects.all()[0]
        self.assertEqual(order.items.count(), 2)

    def test_item_count_after_delete(self):
        order = Order.objects.all()[0]
        MenuInstance.objects.all()[0].delete()
        self.assertEqual(order.items.count(), 1)

    def test_category_property(self):
        kind = MenuItem.objects.get(name='sub')
        sub = MenuInstance.objects.get(kind=kind)
        self.assertEqual(sub.category, 'Subs')










