from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .forms import CustomUserCreationForm


class CustomerDetailView(LoginRequiredMixin, DetailView): 
    model = get_user_model()
    template_name = 'account/customer_detail.html'

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# Create your views here.
