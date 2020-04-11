from django.contrib import admin
from .models import Size, Pasta, PizzaChoice, Sub, Dinner, Topping, Salad, Order, SubChoice, DinnerChoice, Pizza, Customer


class OrderInline(admin.TabularInline):
    model = Order

class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
    ]


admin.site.register(Size)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerChoice)
admin.site.register(SubChoice)
admin.site.register(PizzaChoice)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(Customer, CustomerAdmin)
