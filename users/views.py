from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from orders.models import Order

from .forms import CustomSignupForm, CustomUserCreationForm

class CustomerDetailView(LoginRequiredMixin, DetailView): 
    model = get_user_model()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(customer=self.request.user.pk, is_confirmed=True).order_by('-time_created')
        return context
    template_name = 'account/customer_detail.html'

class SignupPageView(CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'account/signup.html'


