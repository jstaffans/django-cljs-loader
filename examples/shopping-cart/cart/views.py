from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.generic.base import TemplateView
import json

from cart.models import Cart
from cart.serializers import CartSerializer
from cart.forms import CartFormSet


class ShoppingCartView(TemplateView):

    template_name = 'home.html'

    def post(self, request):
        context = self.get_context_data()
        form = CartFormSet(request.POST, instance=self.cart())

        if form.is_valid():
            form.save()

        return JsonResponse({})

    def cart(self):
        return Cart.objects.all()[:1].get()

    def get_context_data(self, **kwargs):
        context = super(ShoppingCartView, self).get_context_data(**kwargs)
        context['cart_json'] = json.dumps(CartSerializer(self.cart()).data)

        # For debugging purposes: see how Django handles form POST
        # context['form'] = CartFormSet(instance=self.cart())

        return context

