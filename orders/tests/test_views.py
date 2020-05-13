from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase, RequestFactory 
from django.urls import reverse, resolve


from orders.models import Category, MenuInstance, Order, MenuItem, Topping
from orders.forms import MenuForm, OrderForm, OrderFormset, MyFormSetHelper



class OrdersViewsTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username = 'prova',
            email = 'prova@prova.it',
            password = 'prova123'
        )
        self.special_permission = Permission.objects.get(codename='special_status')
        self.factory = RequestFactory()
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
            customer = self.user,
            kind = item_pizza,
            size = 'Small',
            n_items = 1,
        )
        pizza.toppings.add(tops1, tops2)
        sub = MenuInstance.objects.create(
            customer = self.user,
            kind = item_sub,
            size = 'Large',
            n_items = 2,
        )
        sub.toppings.add(tops3)
        pizza.n_items = 2
        pizza.save()
        
    def test_menu_view(self):
        self.response = self.client.get(reverse('menu'))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'orders/menu.html')
        self.assertEqual(self.response.context['items'].count(), 4)
        self.assertEqual(self.response.context['toppings'].count(), 3)
        self.assertEqual(self.response.context['categories'].count(), 4)
        self.assertContains(self.response, 'Menu')
        self.assertNotContains(self.response, 'Pippopooppo')

    def test_item_create_view_loggedin(self):
        self.client.login(email='prova@prova.it', password='prova123')
        category = Category.objects.get(name='Subs')
        self.response = self.client.get(reverse('additem', kwargs={'category' : category.slug}))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'orders/item_add.html')
        self.assertEqual(self.response.context['items'].count(), 1)
        self.assertEqual(self.response.context['toppings'].count(), 0)
        self.assertEqual(self.response.context['categories'].count(), 4)
        self.assertEqual(self.response.context['category'], category)

    def test_item_create_view_loggedout(self):
        self.client.logout
        category = Category.objects.get(name='Subs')
        response = self.client.get(reverse('additem', kwargs={'category' : category.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/orders/item/subs' % (reverse('account_login'))) 
        response = self.client.get('%s?next=//orders/item/subs' % (reverse('account_login'))) 
        self.assertContains(response, 'Log In')

    def test_item_create_form_view(self):
        self.client.login(email='prova@prova.it', password='prova123')
        sub = MenuItem.objects.get(name='sub')
        category = Category.objects.get(name='Subs')
        user = get_user_model().objects.get(username='prova')
        request = self.factory.get(reverse('additem', kwargs={'category' : category.slug}))
        request.user = user
        form = MenuForm(data={'kind': str(sub.pk), 'size': 'Small', 'n_items': 2}, category=category.slug)
        form.instance.customer = request.user
        self.assertTrue(form.is_valid())

    def test_item_create_view_using_post(self):
        sub = MenuItem.objects.get(name='sub')
        category = Category.objects.get(name='Subs')
        user = get_user_model().objects.get(username='prova')
        request = self.factory.get(reverse('additem', kwargs={'category' : category.slug}))
        request.user = user
        self.client.login(email='prova@prova.it', password='prova123')
        response = self.client.post(reverse('additem', kwargs={'category' : category.slug}), {'kind': str(sub.pk), 'size': 'Small', 'n_items': 2, 'customer': request.user})
        self.assertRedirects(response, reverse('menu'))   

    def test_order_list_view_loggin_no_permission(self):
        self.client.login(email='prova@prova.it', password='prova123')
        self.response = self.client.get(reverse('order-list'))
        self.assertEqual(self.response.status_code, 403)

    def test_order_list_view_loggin_with_permission(self):
        self.client.login(email='prova@prova.it', password='prova123')
        self.user.user_permissions.add(self.special_permission)
        self.response = self.client.get(reverse('order-list'))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'orders/order_list.html')
        self.assertEqual(self.response.context['orders'].count(), 1)

    def test_order_detail_view_no_permissions(self):
        order = Order.objects.all()[0]
        self.client.login(email='prova@prova.it', password='prova123')
        self.response = self.client.get(order.get_absolute_url())
        self.assertEqual(self.response.status_code, 403)

    def test_order_detail_view_with_permissions(self):
        order = Order.objects.all()[0]
        self.client.login(email='prova@prova.it', password='prova123')
        self.user.user_permissions.add(self.special_permission)
        self.response = self.client.get(order.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'orders/order_detail.html')
        self.assertContains(self.response, 'Order')
        self.assertNotContains(self.response, 'Pippopooppo')

    def test_order_edit_view_no_permissions(self):
        order = Order.objects.all()[0]
        self.client.login(email='prova@prova.it', password='prova123')
        self.response = self.client.get(reverse('order-edit', kwargs={'pk' : order.pk}))
        self.assertEqual(self.response.status_code, 403)

    

    def test_order_edit_view_with_permission_using_form(self):
        order = Order.objects.all()[0]
        self.client.login(email='prova@prova.it', password='prova123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(reverse('order-edit', kwargs={'pk' : order.pk}))
        form = OrderForm(data={'order_state': "Done", 'final_price': order.final_price})
        self.assertTrue(form.is_valid())
        self.assertTemplateUsed(response, 'orders/order_edit.html')
        self.assertContains(response, 'Order')
        self.assertNotContains(response, 'Pippopooppo')

    def test_order_edit_view_with_permission_using_post(self):
        order = Order.objects.all()[0]
        self.client.login(email='prova@prova.it', password='prova123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.post(reverse('order-edit', kwargs={'pk' : order.pk,}), {'order_state': "Done", 'final_price': order.final_price})
        self.assertRedirects(response, reverse('order-list'))


    def test_cart_update_view_loggedout(self):
        order = Order.objects.all()[0]
        self.response = self.client.get(reverse('cart', kwargs={'pk' : order.pk}))
        self.assertEqual(self.response.status_code, 302)
        self.assertTrue(self.response.url.startswith('/accounts/login/'))

    def test_order_edit_view_wrong_id(self):
        self.client.login(email='prova@prova.it', password='prova123')
        self.user.user_permissions.add(self.special_permission)
        self.response = self.client.get(reverse('order-edit', kwargs={'pk' : 123}))
        self.assertEqual(self.response.status_code, 404)

    def test_cart_update_view_with_permission_using_form(self):
        order = Order.objects.all()[0]
        items = []
        for item in MenuInstance.objects.all():
            items.append(item)
        self.client.login(email='prova@prova.it', password='prova123')
        response = self.client.get(reverse('cart', kwargs={'pk' : order.pk}))
        formset = OrderFormset({
            'items-INITIAL_FORMS': '2',
            'items-TOTAL_FORMS': '2',
            'items-MAX_NUM_FORMS': '',
            'items-0-kind': items[1].kind.pk,
            'items-0-size': 'Small',
            'items-0-n_items': '1',
            'items-0-id': items[1].pk,
            'items-1-kind': items[0].kind.pk,
            'items-1-size': 'Large',
            'items-1-n_items': '2',
            'items-1-id': items[0].pk,
        })
        self.assertTrue(formset.is_valid())
        self.assertTemplateUsed(response, 'orders/shoppingcart.html')
        self.assertContains(response, 'Cart')
        self.assertNotContains(response, 'Pippopooppo')
        self.assertTrue(response.context['order'], order)
        self.assertTrue(response.context['item'], formset)
        self.assertTrue(response.context['item'], MyFormSetHelper())


    '''def test_cart_update_view_with_permission_using_post(self):
        order = Order.objects.all()[0]
        items = []
        for item in MenuInstance.objects.all():
            items.append(item)
        self.client.login(email='prova@prova.it', password='prova123')
        response = self.client.get(reverse('cart', kwargs={'pk' : order.pk}))
        formset = OrderFormset({
            'items-INITIAL_FORMS': '2',
            'items-TOTAL_FORMS': '2',
            'items-MAX_NUM_FORMS': '',
            'items-0-kind': items[1].kind.pk,
            'items-0-size': 'Small',
            'items-0-n_items': '1',
            'items-0-id': items[1].pk,
            'items-1-kind': items[0].kind.pk,
            'items-1-size': 'Large',
            'items-1-n_items': '2',
            'items-1-id': items[0].pk,
        })
        response = self.client.post(reverse('order-edit', kwargs={'pk' : order.pk,}), {'order_state': "Done", 'final_price': order.final_price})
        self.assertRedirects(response, reverse('order-list'))'''

    