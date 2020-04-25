from django.contrib import admin
from .models import Category, Customer, MenuItem ,MenuInstance, Order, Topping

class OrderInline(admin.TabularInline):
    model = MenuInstance

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
    ]

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Topping)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer)

