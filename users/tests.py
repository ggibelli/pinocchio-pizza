from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve, reverse_lazy

from orders.models import Order
from .forms import CustomSignupForm


class CustomUserTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'prova',
            email = 'prova@prova.it',
            password = 'prova123'
        )
        self.assertEqual(user.username, 'prova')
        self.assertEqual(user.email, 'prova@prova.it')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username = 'superprova',
            email = 'superprova@prova.it',
            password = 'prova123'
        )
        self.assertEqual(admin_user.username, 'superprova')
        self.assertEqual(admin_user.email, 'superprova@prova.it')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class SignupTests(TestCase):

    username = 'usertest'
    email = 'usertest@email.it'
    first_name = 'gio'
    last_name = 'gah'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)
        self.factory = RequestFactory()

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Pippopooppo')

    def test_signup_form(self): 
        new_user = get_user_model().objects.create_user(username = self.username, email = self.email, first_name = self.first_name, last_name = self.last_name)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        self.assertEqual(get_user_model().objects.all()[0].first_name, self.first_name)
        self.assertEqual(get_user_model().objects.all()[0].last_name, self.last_name)

    def test_custom_signup_form(self):
        user_count = get_user_model().objects.count()
        response = self.client.post(reverse('account_signup'), {'email' : 'prova@prova.it', 'first_name': 'gio', 'last_name': 'gibe', 'password1': 'ProvaTest123', 'password2': 'ProvaTest123'})
        self.assertEqual(get_user_model().objects.get(email='prova@prova.it').last_name, 'gibe')
        self.assertRedirects(response, reverse_lazy('home')) 
        self.assertEqual(get_user_model().objects.count(), user_count+1)

class CustomerDetailViewTests(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'prova',
            email = 'prova@prova.it',
            password = 'prova123'
        )
        order = Order.objects.create(customer=user, is_confirmed=True, final_price=0)

    def test_customer_detail_template_loggedin(self):
        self.client.login(email='prova@prova.it', password='prova123')
        user = get_user_model().objects.get(username='prova')
        self.response = self.client.get(reverse('profile', kwargs={'slug' : user.slug}))
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context['orders'].count(), 1)
        self.assertTemplateUsed(self.response, 'account/customer_detail.html')
        self.assertContains(self.response, 'My orders')
        self.assertNotContains(self.response, 'Pippopooppo')

    def test_customer_detail_template_loggedout(self):
        self.client.logout()
        response = self.client.get(reverse('profile', kwargs={'slug' : 'prova'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/users/prova/' % (reverse('account_login'))) 
        response = self.client.get('%s?next=/users/prova/' % (reverse('account_login'))) 
        self.assertContains(response, 'Log In')