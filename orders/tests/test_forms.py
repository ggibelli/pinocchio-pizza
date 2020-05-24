from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from orders.models import Category, MenuInstance, Order, MenuItem, Topping
from orders.forms import MenuForm, OrderForm, OrderFormset, MyFormSetHelper

class MenuFormTest(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'prova',
            email = 'prova@prova.it',
            password = 'prova123'
        )
        category = Category.objects.create(name='Subs')
        category2 = Category.objects.create(name='Salad')
        category3 = Category.objects.create(name='Pizza')
        sub = MenuItem.objects.create(
            name = 'bbb',
            category=category,
            price = 5.0,
            price_large = 10.0
        )
        salad = MenuItem.objects.create(
            name = 'ccc',
            category=category2,
            price = 20.0,
            price_large = 25.0
        )
        pizza = MenuItem.objects.create(
            name = 'ddd',
            category=category3,
            price = 22.0,
            price_large = 24.0
        )
        tops1 = Topping.objects.create(name='abc', is_topping_subs=True)
        tops2 = Topping.objects.create(name='bac')
        tops3 = Topping.objects.create(name='cab')
        instance1 = MenuInstance.objects.create(
            customer = user,
            dish = sub,
            size = 'Large',
            n_items = 2,
        )
        

    def test_menu_instance_create_valid_sub(self, **kwargs):
        sub = MenuItem.objects.get(name='bbb')
        user = get_user_model().objects.get(username='prova')
        category = Category.objects.get(name='Subs')
        topping = Topping.objects.get(name='abc')
        form = MenuForm(data={'dish': str(sub.pk), 'size': 'Small', 'toppings': [topping.pk], 'n_items': 2}, category=category.slug)
        form.instance.customer = user
        self.assertTrue(form.is_valid())

    def test_menu_instance_create_valid_pizza(self, **kwargs):
        pizza = MenuItem.objects.get(name='ddd')
        user = get_user_model().objects.get(username='prova')
        category = Category.objects.get(name='Pizza')
        topping = Topping.objects.get(name='bac')
        form = MenuForm(data={'dish': str(pizza.pk), 'size': 'Small', 'toppings':[topping.pk], 'n_items': 2}, category=category.slug)
        form.instance.customer = user
        self.assertTrue(form.is_valid())

    def test_menu_instance_create_valid_salad(self, **kwargs):
        salad = MenuItem.objects.get(name='ccc')
        user = get_user_model().objects.get(username='prova')
        category = Category.objects.get(name='Salad')
        form = MenuForm(data={'dish': str(salad.pk), 'size': 'Small', 'n_items': 2}, category=category.slug)
        form.instance.customer = user
        self.assertTrue(form.is_valid())

    def test_menu_instance_create_invalid_sub(self, **kwargs):
        sub = MenuItem.objects.get(name='bbb')
        user = get_user_model().objects.get(username='prova')
        category = Category.objects.get(name='Subs')
        topping = Topping.objects.get(name='bac')
        form = MenuForm(data={'dish': str(sub.pk), 'size': 'Small', 'toppings': [topping.pk], 'n_items': 2}, category=category.slug)
        form.instance.customer = user
        self.assertFalse(form.is_valid())

    def test_menu_instance_create_invalid_pizza(self, **kwargs):
        pizza = MenuItem.objects.get(name='ccc')
        user = get_user_model().objects.get(username='prova')
        category = Category.objects.get(name='Pizza')
        topping = Topping.objects.get(name='bac')
        form = MenuForm(data={'dish': str(pizza.pk), 'size': 'Small', 'toppings':[topping.pk], 'n_items': 2}, category=category.slug)
        form.instance.customer = user
        self.assertFalse(form.is_valid())

    def test_menu_instance_create_invalid_salad(self, **kwargs):
        salad = MenuItem.objects.get(name='ccc')
        user = get_user_model().objects.get(username='prova')
        category = Category.objects.get(name='Salad')
        form = MenuForm(data={'dish': str(salad.pk), 'size': 'Small', 'n_items': -2}, category=category.slug)
        form.instance.customer = user
        self.assertFalse(form.is_valid())

    def test_orderformset_valid(self, **kwargs):
        dish = MenuItem.objects.get(name='bbb')
        order = Order.objects.all()[0]
        formset = OrderFormset({
            'items-INITIAL_FORMS': '1',
            'items-TOTAL_FORMS': '1',
            'items-MAX_NUM_FORMS': '',
            'items-0-dish': dish.pk,
            'items-0-size': 'Small',
            'items-0-n_items': '2',
            'items-0-id': order.pk,
        })
        self.assertTrue(formset.is_valid())

    def test_orderformset_not_valid(self, **kwargs):
        dish = MenuItem.objects.get(name='bbb')
        order = Order.objects.all()[0]
        formset = OrderFormset({
            'items-INITIAL_FORMS': '1',
            'items-TOTAL_FORMS': '1',
            'items-MAX_NUM_FORMS': '',
            'items-0-dish': dish.pk,
            'items-0-size': 'Small',
            'items-0-n_items': '-2',
            'items-0-id': order.pk,
        })
        self.assertFalse(formset.is_valid())
    