from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple

from .models import MenuInstance, Order, Topping

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuInstance
        fields = ['kind', 'size', 'toppings', 'n_items', 'final_price']
    def __init__(self, *args, **kwargs):

        super(MenuForm, self).__init__(*args, **kwargs)

        self.fields["toppings"].widget = CheckboxSelectMultiple()
        self.fields["toppings"].queryset = Topping.objects.all()

OrderFormset = inlineformset_factory(
    Order, MenuInstance, fields=('n_items', 'size', 'final_price'), extra=0)