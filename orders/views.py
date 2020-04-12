from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Customer
from django.contrib.auth import get_user_model

# Create your views here.

class CustomerDetailView(LoginRequiredMixin, DetailView): 
    model = get_user_model()
    template_name = 'orders/customer_detail.html'

