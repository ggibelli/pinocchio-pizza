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
        category4 = Category.objects.create(name='Pizza')
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
        dishes = MenuItem.objects.all()
        self.assertEqual(len(dishes), 4)

    def test_is_valid_price_large(self):
        sub = MenuItem.objects.get(name='sub')
        self.assertTrue(sub.is_valid_price())

    def test_is_valid_price_small(self):
        salad = MenuItem.objects.get(name='salad')
        self.assertTrue(salad.is_valid_price())

    def test_is_valid_str_menuitem(self):
        salad = MenuItem.objects.get(name='salad')
        self.assertEqual(str(salad), salad.name)

    def test_is_valid_str_topping(self):
        topping = Topping.objects.get(name='abc')
        self.assertEqual(str(topping), topping.name)

    def test_is_valid_str_menuinstance(self):
        kind = MenuItem.objects.get(name='pizza')
        pizza = MenuInstance.objects.get(kind=kind)
        self.assertEqual(str(pizza), pizza.kind.name)

    def test_is_valid_str_order(self):
        order = Order.objects.all()[0]
        self.assertEqual(str(order), f'{order.id} ({order.time_created})')

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
        category = Category.objects.get(name='Subs')
        sub = MenuInstance.objects.get(kind=kind)
        self.assertEqual(sub.category, category.name)
        self.assertEqual(kind.category, category)

    def test_category_count_dishes(self):
        category = Category.objects.get(name='Salad')
        self.assertEqual(category.dishes.count(), 1)









