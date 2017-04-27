import uuid
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Cart(BaseModel):
    pass


class Item(BaseModel):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, related_name='items')

