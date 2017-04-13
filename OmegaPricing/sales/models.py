from django.db import models

from core.models import TimeStampedModel
from sales.exceptions import ProductMisMatch

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProductManager(models.Manager):
    # usually I extract these managers out to their own file but just to keep things concise

    def update_product(self, product_data):
        # first get product with same external ID
        try:
            existing_product = self.get(
                external_product_id=product_data['id']
            )
            name_matches = existing_product.name == product_data['name']
            price_matches = existing_product.price_in_pennies == int(product_data['price'])
            if name_matches and not price_matches:
                percentage_change = existing_product.price_in_pennies - int(product_data['price'])
                percentage_change = percentage_change / existing_product.price_in_pennies
                percentage_change = percentage_change * 100

                # could maybe make sure these updates/saves are atomic but for simplicities sake I am not.
                PastPriceRecord.objects.create(
                    product=existing_product,
                    price_in_pennies=existing_product.price_in_pennies,
                    percentage_change=float(percentage_change)
                )

                # update the existing product
                existing_product.price_in_pennies = product_data['price']
                existing_product.save()
            elif not name_matches:
                msg = "existing product '{0}' does not match external product name '{1}'".format(
                    existing_product.name, product_data['name']
                )
                raise ProductMisMatch(msg)
        except self.model.DoesNotExist:
            if not product_data['discontinued']:
                self.create(
                    name=product_data['name'],
                    price_in_pennies=product_data['price'],
                    external_product_id=product_data['id']
                )
                msg = """A new product was created! name: {0}, price: {1}, external_product_id: {2}
                """.format(product_data['name'], product_data['price'], product_data['id'])
                # django logging levevl seems to eat INFO debug level. You'd probably want
                # to log to a file or some external logging tool but for this will suffice
                # for the pruproses of this demonstration
                logger.warning(msg=msg)


class Product(TimeStampedModel):
    # Assume that the external product id is unique
    external_product_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)  # I assume length is okay.
    price_in_pennies = models.PositiveIntegerField()

    objects = ProductManager()


class PastPriceRecord(TimeStampedModel):
    product = models.ForeignKey(Product)
    price_in_pennies = models.PositiveIntegerField(null=False)
    percentage_change = models.FloatField(default=0.0)
