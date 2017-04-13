from rest_framework import serializers


class OmegaProductSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=True)
    name = serializers.CharField()
    price = serializers.CharField()
    discontinued = serializers.BooleanField()
    category = serializers.CharField()

    def validate_price(self, value):
        value = round(float(value.strip('$'))*100)
        return value
