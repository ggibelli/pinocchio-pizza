from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, ListView, TemplateView, UpdateView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import MenuForm, OrderFormset
from .models import Category, Customer, MenuItem, MenuInstance, Order, Topping


class MultipleModelView(TemplateView):
    template_name = 'orders/menu.html'

    def get_context_data(self, **kwargs):
        context = super(MultipleModelView, self).get_context_data(**kwargs)
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
        context = super(CreateView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # get the category from url for queryset context
        category = Category.objects.get(name=(self.kwargs['category']))
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

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders/order_list.html'

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_detail.html'

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['order_state']
    template_name = 'orders/shoppingcart.html'
    def get_object(self):
        try:
            return Order.objects.get(customer=self.request.user.pk, order_state='CT')
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['item'] = OrderFormset(self.request.POST, instance=self.object)
        else:
            data['item'] = OrderFormset(instance=self.object)
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        item = context['item']
        self.object = form.save()
        if item.is_valid():
            item.instance = self.object
            item.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('order-list')

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order-list')


