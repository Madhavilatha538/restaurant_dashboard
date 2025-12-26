from django import forms
from restaurant.models import Table, MenuItem
from .models import Order, OrderItem

class OrderCreateForm(forms.Form):
    table = forms.ModelChoiceField(queryset=Table.objects.all().order_by("number"))
    # dynamic items in view

class OrderItemForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.filter(is_available=True).order_by("category","name"))
    quantity = forms.IntegerField(min_value=1, initial=1)
