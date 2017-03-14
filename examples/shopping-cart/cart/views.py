from django.forms.models import model_to_dict
from django.views.generic.base import TemplateView
from edn_format.edn_lex import Keyword
import edn_format
import json

from cart.models import Cart
from cart.serializers import CartSerializer


class ShoppingCartView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(ShoppingCartView, self).get_context_data(**kwargs)
        cart = Cart.objects.all()[:1].get()
        context['initial_props'] = edn_format.dumps(CartSerializer(cart).data)
        return context
