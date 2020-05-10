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
        

    def test_menu_instance_create_valid(self, **kwargs):
        sub = MenuItem.objects.get(name='bbb')
        user = get_user_model().objects.get(username='prova')
        category = Category.objects.get(name='Subs')
        form = MenuForm(data={'kind': str(sub.pk), 'size': 'Small', 'n_items': 2}, category=category.slug)
        form.instance.customer = user
        self.assertTrue(form.is_valid())