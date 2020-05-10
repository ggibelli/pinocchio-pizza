from django.contrib import admin
from .models import Category, MenuItem ,MenuInstance, Order, Topping

class OrderInline(admin.TabularInline):
    model = MenuInstance

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id', 'customer', 'order_state', 'final_price']
    list_filter = ('order_state', 'customer__username')
    inlines = [
        OrderInline,
    ]

class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem
    list_display = ['name', 'category', 'price', 'price_large']
    list_filter = ('category__name',)

admin.site.register(Category)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Topping)
admin.site.register(Order, OrderAdmin)
admin.site.register(MenuInstance)


