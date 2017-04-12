from django.db import models

from core.models import TimeStampedModel


class Product(TimeStampedModel):
    external_product_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)  # I assume length is okay.
    price_in_pennies = models.PositiveIntegerField()


class PastPriceRecords(TimeStampedModel):
    product = models.ForeignKey(Product)
    price_in_pennies = models.PositiveIntegerField()
    percentage_change = models.FloatField()
