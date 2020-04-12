from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from orders.models import Order

from .forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()

class OrderInline(admin.TabularInline):
    model = Order  

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username','slug']
    inlines = [
        OrderInline,
    ]

admin.site.register(CustomUser, CustomUserAdmin)

