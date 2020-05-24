from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Layout, Field, Fieldset
from crispy_forms.bootstrap import *


from .models import Category, MenuItem, MenuInstance, Order, Topping

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuInstance
        fields = ['dish', 'size', 'toppings', 'n_items']
        dish = forms.ModelChoiceField(queryset=MenuItem.objects.none())
    # get the category from the url and query only the item in that category (kwargs.pop)    
    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category')
        category_id = Category.objects.get(slug=category)
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['dish'].queryset = MenuItem.objects.filter(category=category_id)
        self.fields['toppings'].widget = CheckboxSelectMultiple()
        if category == 'pasta' or category == 'salad' or category == 'dinner-platters':
            self.fields['toppings'].widget = forms.HiddenInput()
            if category == 'salad' or category == 'pasta':
                self.fields['size'].widget = forms.HiddenInput()
        elif category == 'subs':
            self.fields["toppings"].queryset = Topping.objects.filter(is_topping_subs=True)
        else:
            self.fields["toppings"].queryset = Topping.objects.all()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_state', 'final_price']

class CartForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_confirmed']
        widgets = {'is_confirmed': forms.HiddenInput()}
               
OrderFormset = inlineformset_factory(
    Order, MenuInstance, fields=('dish', 'size', 'n_items'), widgets={'dish': forms.HiddenInput()}, extra=0)

class MyFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MyFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Field('dish'),
            Field('size', css_class='size'),
            Field('n_items', css_class='items'),
            
        )
        self.form_tag = False
        self.template = 'orders/table_inline_formset.html'
