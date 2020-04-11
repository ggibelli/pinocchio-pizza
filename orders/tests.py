from django.test import TestCase
from .models import Size, Pasta, PizzaChoice, Sub, Dinner, Topping, Salad, Order, SubChoice, DinnerChoice, Pizza
from .prices import price_pizza, price_dinner, price_sub, price_order
from django.contrib.auth import get_user_model


class SizeTest(TestCase):

    def test_create_size(self):
        size = Size.objects.create(size='SM')
        self.assertEqual(size.size, 'SM')

class SimpleDishesTest(TestCase):

    def test_pasta_salad(self):
        pasta = Pasta.objects.create(name='Penne', final_price=10.00)
        salad = Salad.objects.create(name='Tuna', final_price=8.00)
        self.assertEqual(pasta.final_price, 10.00)
        self.assertEqual(pasta.name, 'Penne')
        self.assertEqual(salad.name, 'Tuna')
        self.assertEqual(salad.final_price, 8.00)

class DishesChoicesTest(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'prova',
            email = 'prova@prova.it',
            password = 'prova123'
        )
        size = Size.objects.create(size='SM')
        pizza_choice = PizzaChoice.objects.create(
            name = 'aaa', 
            price_regular = 2.5, 
            price_sicilian = 8.5,
            price_large = 5.0,
            price_sicilian_large = 10.5
        )
        sub_choice = SubChoice.objects.create(
            name = 'bbb',
            price = 5.0,
            price_large = 10.0
        )
        dinner_choice = DinnerChoice.objects.create(
            name = 'ccc',
            price = 20.0,
            price_large = 25.0
        )
        tops1 = Topping.objects.create(name='abc')
        tops2 = Topping.objects.create(name='bac')
        tops3 = Topping.objects.create(name='cab')
        pizza = Pizza.objects.create(
            pizza_type = pizza_choice,
            is_sicilian = True,
            size = size,
            final_price = 8.5
        )
        pizza.toppings.add(tops1, tops2)
        sub = Sub.objects.create(
            sub_type = sub_choice,
            size = size,
            final_price = 5
        )
        sub.toppings.add(tops3)
        dinner = Dinner.objects.create(
            dinner_type = dinner_choice,
            size = size,
            final_price = 20
        )
        pasta = Pasta.objects.create(name='Penne', final_price=10.00)
        salad = Salad.objects.create(name='Tuna', final_price=8.00)
        order = Order.objects.create(
            customer_id = user,
            final_price = 51.5
        )
        order.item_pizza.add(pizza)
        order.item_subs.add(sub)
        order.item_dinner.add(dinner)
        order.item_salad.add(salad)
        order.item_pasta.add(pasta)

    def test_dishes_count(self):
        self.assertEqual(PizzaChoice.objects.count(), 1)
        self.assertEqual(SubChoice.objects.count(), 1)
        self.assertEqual(DinnerChoice.objects.count(), 1)

    def test_is_valid_pizza(self):
        pizza = PizzaChoice.objects.get(name='aaa')
        self.assertTrue(pizza.is_valid_price())

    def test_is_valid_sub(self):
        sub = SubChoice.objects.get(name='bbb')
        self.assertTrue(sub.is_valid_price())

    def test_is_valid_dinner(self):
        dinner = DinnerChoice.objects.get(name='ccc')
        self.assertTrue(dinner.is_valid_price())

    def test_is_pizza_right_price(self):
        pizza = Pizza.objects.all()[0]
        self.assertEqual(pizza.final_price, price_pizza(pizza))
        self.assertTrue(pizza.is_valid_price())

    def test_pizza_ntoppings(self):
        pizza = Pizza.objects.all()[0]
        self.assertEqual(pizza.toppings.count(), 2)

    def test_is_sub_right_price(self):
        sub = Sub.objects.all()[0]
        self.assertEqual(sub.final_price, price_sub(sub))
        self.assertTrue(sub.is_valid_price())

    def test_pizza_ntoppings(self):
        sub = Sub.objects.all()[0]
        self.assertEqual(sub.toppings.count(), 1)

    def test_is_dinner_right_price(self):
        dinner = Dinner.objects.all()[0]
        self.assertEqual(dinner.final_price, price_dinner(dinner))
        self.assertTrue(dinner.is_valid_price())

    def test_order_right_price(self):
        order = Order.objects.all()[0]
        self.assertEqual(order.final_price, price_order(order))
        self.assertTrue(order.is_valid_price())

    def test_order_user(self):
        order = Order.objects.all()[0]
        user = get_user_model().objects.all()[0]
        self.assertEqual(order.customer_id, user)

    def test_order_user_count(self):
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.orders.count(), 1)






