import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.views.generic import CreateView, DetailView, DeleteView, FormView, ListView, TemplateView, UpdateView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CartForm, MenuForm, OrderForm, OrderFormset, MyFormSetHelper
from .models import Category, MenuItem, MenuInstance, Order, Topping


class MultipleModelView(TemplateView):
    template_name = 'orders/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = MenuItem.objects.all()
        context['toppings'] = Topping.objects.all()
        context['categories'] = Category.objects.all()
        return context

class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'orders/item_add.html'
    model = MenuInstance
    form_class = MenuForm
    success_url = reverse_lazy('menu')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # get the category from url for queryset context
        category = Category.objects.get(slug=(self.kwargs['category']))
        if category == Category.objects.get(name='Subs'):
            context['toppings'] = Topping.objects.filter(is_topping_subs=True)
        context['items'] = MenuItem.objects.filter(category=category)
        context['category'] = Category.objects.get(name=category)
        return context
    #get the kwargs from the url for the __init__ in forms
    def get_form_kwargs(self):
        kwargs = super(CreateView,self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    queryset = Order.objects.order_by('-time_created')
    context_object_name = 'orders'
    permission_required = 'orders.special_status'
    template_name = 'orders/order_list.html'

class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    permission_required = 'orders.special_status'
    template_name = 'orders/order_detail.html'

class OrderEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    context_object_name = 'order'
    permission_required = 'orders.special_status'
    form_class = OrderForm
    template_name = 'orders/order_edit.html'
    success_url = reverse_lazy('order-list')
    
class CartUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = CartForm
    template_name = 'orders/shoppingcart.html'
    def get_object(self):
        try:
            return Order.objects.get(customer=self.request.user.pk, is_confirmed=False)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object
        context['helper'] = MyFormSetHelper()
        if self.request.POST:
            context['item'] = OrderFormset(self.request.POST, instance=self.object)
        else:
            context['item'] = OrderFormset(instance=self.object)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        item = context['item']
        self.object = form.save()
        if item.is_valid():
            item.instance = self.object
            item.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        if self.object.items.count() == 0:
            Order.objects.get(id=self.object.id).delete()
            return reverse_lazy('menu')
        return reverse_lazy('confirm-cart', kwargs={'pk' : self.object.pk})

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order-list')

class ConfirmOrderView(LoginRequiredMixin, DetailView):
    model = Order
    def get_object(self):
        try:
            return Order.objects.get(customer=self.request.user.pk, is_confirmed=False)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
    object_name = 'order'
    template_name = 'orders/confirm_order.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context

def charge(request): 
    if request.method == 'POST':
        amount = request.POST.get('order-amount')
        order = Order.objects.get(id=request.POST.get('order-id'))
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd', 
                description='Pizzeria dish', 
                source=request.POST.get('stripeToken')
                )
            order.is_confirmed = True
            order.save()
            subject = f'Thanks for your order n. {order.id} of {order.final_price}$'
            message = f"Your order was processed correctly, \nyou'll receive a second email when ready"
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [order.customer.email,]
            send_mail( subject, message, email_from, recipient_list )
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            #body = e.json_body
            #err  = body.get('error', {})
            
            # Attach the entire error string as JSON
            messages.error(request, e.error.message)
        except stripe.error.RateLimitError as e:
            messages.error(request, 'Rate limit error')
        except stripe.error.InvalidRequestError as e:
            messages.error(request, 'Invalid parameter')
        except stripe.error.AuthenticationError as e:
            messages.error(request, 'Not authenticated')
        except stripe.error.APIConnectionError as e:
            messages.error(request, 'Network error')
        except stripe.error.StripeError as e:
            messages.error(request, 'Something wrong, please try again')

        return redirect('post_payment', cart_id = order.id)

def post_payment(request, cart_id):
    template = 'orders/charge.html'
    context = {}

    storage = messages.get_messages(request)
    for message in storage:

        context['message'] = message.message
        context['cart_id'] = cart_id

    return render(request, template, context)



