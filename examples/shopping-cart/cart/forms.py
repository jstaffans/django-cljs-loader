from django.forms.models import inlineformset_factory
from django import forms

from cart.models import Cart, Item

CartFormSet = inlineformset_factory(
    Cart,
    Item,
    fields='__all__'
)
