from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, ListView, TemplateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import MenuForm
from .models import Customer, MenuItem, MenuInstance, Order, Topping

# Create your views here.

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
        context_object_name = 'orders'
    template_name = 'orders/order_list.html'

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['final_price']
    template_name = 'orders/shoppingcart.html'
    def get_object(self):
        return Order.objects.get(customer=self.request.user.pk, order_state='CT')
    def get_context_data(self, **kwargs):
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

class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order-list')

class MultipleModelView(TemplateView):
    template_name = 'orders/menu.html'

    def get_context_data(self, **kwargs):
         context = super(MultipleModelView, self).get_context_data(**kwargs)
         context['items'] = MenuItem.objects.all()
         context['toppings'] = Topping.objects.all()
         return context

class ItemCreateView(CreateView):
    template_name = 'orders/item_add.html'
    model = MenuInstance
    form_class = MenuForm
    success_url = reverse_lazy('pizza')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        if form.instance.final_price != form.instance.get_price():
            form.instance.final_price = form.instance.get_price()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['items'] = MenuChoice.objects.all()
        return context

