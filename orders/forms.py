from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple

from .models import Category, MenuItem, MenuInstance, Order, Topping

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuInstance
        fields = ['kind', 'size', 'toppings', 'n_items']
        kind = forms.ModelChoiceField(queryset=MenuItem.objects.none())
    # get the category from the url and query only the item in that category (kwargs.pop)    
    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category')
        category_id = Category.objects.get(name=category)
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['kind'].queryset = MenuItem.objects.filter(category=category_id)
        self.fields['toppings'].widget = CheckboxSelectMultiple()
        if category == 'Pasta' or category == 'Salad' or category == 'Dinner':
            self.fields['toppings'].widget = forms.HiddenInput()
        elif category == 'Subs':
            self.fields["toppings"].queryset = Topping.objects.filter(is_topping_subs=True)
        else:
            self.fields["toppings"].queryset = Topping.objects.all()
               
OrderFormset = inlineformset_factory(
    Order, MenuInstance, fields=('kind', 'n_items', 'size'), extra=0)