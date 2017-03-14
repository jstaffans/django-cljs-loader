from django.core.management.base import BaseCommand

from cart.models import Item, Cart

class Command(BaseCommand):

    def handle(self, *args, **opts):
        cart = Cart.objects.create()
        cart.save()

        apples = Item.objects.create(
            name="Apple",
            quantity=3,
            cart=cart
        )
        apples.save()

        oranges = Item.objects.create(
            name="Orange",
            quantity=5,
            cart=cart
        )
        oranges.save()

        soda = Item.objects.create(
            name="Soda",
            quantity=2,
            cart=cart
        )
        soda.save()

