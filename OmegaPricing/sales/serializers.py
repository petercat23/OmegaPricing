from rest_framework import serializers
from sales.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'external_product_id', 'price_in_pennies')


class OmegaProductSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=True)
    name = serializers.CharField()
    price = serializers.CharField()
    discontinued = serializers.BooleanField()
    category = serializers.CharField()

    def validate_price(self, value):
        value = int(round(float(value.strip('$'))*100))
        return value
