from django.contrib.auth import get_user_model
from django.test import TestCase


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

