import requests
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response

from sales.serializers import OmegaProductSerializer
from sales.models import Product
from sales.exceptions import ProductMisMatch

import logging
logger = logging.getLogger(__name__)


# one could argue that this should be a POST request
class GetUpdatedSalesRecords(views.APIView):

    def get_payload(self):
        # Time can get real weird so I'm assuming this will suffice
        now = datetime.utcnow()
        one_month_ago = now - timedelta(days=30)
        return {
            'api_key': settings.OMEGA_API_KEY,
            'start_date': one_month_ago,
            'end_date': now
        }

    def get(self, request, *args, **kwargs):
        url = settings.OMEGA_PRCICING_URL
        payload = self.get_payload()
        omega_response = requests.get(url, params=payload)

        data = omega_response.json()

        if omega_response.status_code != 200:
            return Response({'detail': data}, status=omega_response.status_code)

        product_records = data.get('product_records')
        if not product_records:
            return Response(
                {'detail': 'json response contained no "product_records" key'},
                status=status.HTTP_404_NOT_FOUND)

        for record in product_records:
            serializer = OmegaProductSerializer(data=record)
            serializer.is_valid(raise_exception=True)
            try:
                Product.objects.update_product(serializer.data)
            except ProductMisMatch as e:
                logger.error(e)

        return Response(serializer.data, status=status.HTTP_200_OK)
