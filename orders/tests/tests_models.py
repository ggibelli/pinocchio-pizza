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
        category2 = Category.objects.create(name='Salad')
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
        )
        pizza.toppings.add(tops1, tops2)
        sub = MenuInstance.objects.create(
            customer = user,
            kind = sub,
            size = 'Large',
            n_items = 2,
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

    def test_menu_view(self):
        self.response = self.client.get(reverse('menu'))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'orders/menu.html')
        self.assertEqual(self.response.context['items'].count(), 2)
        self.assertEqual(self.response.context['toppings'].count(), 3)
        self.assertEqual(self.response.context['categories'].count(), 2)
        self.assertContains(self.response, 'Menu')
        self.assertNotContains(self.response, 'Pippopooppo')

    def test_item_create_view(self):
        self.client.login(email='prova@prova.it', password='prova123')
        category = Category.objects.get(name='Subs')
        self.response = self.client.get(reverse('additem', kwargs={'category' : category.slug}))
        self.assertEqual(self.response.status_code, 200)







