import mock
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from sales.models import Product, PastPriceRecord


class SalesTests(APITestCase):

    url_update_sales_records = reverse('updateSales')

    mock_data = {
        'product_records': [
            {
                "id": 123456,
                "name": "Nice Chair",
                "price": "$30.25",
                "category": "home-furnishings",
                "discontinued": False
            },
            {
                "id": 234567,
                "name": "Black & White TV",
                "price": "$43.77",
                "category": "electronics",
                "discontinued": True
            }
        ]
    }

    def mocked_requests_get(self, *args, **kwargs):
        class MockResponse:
            def __init__(self, data, status_code):
                self.data = data
                self.status_code = status_code

            def json(self):
                return self.data
        return MockResponse(self.mock_data, 200)

    def test_get_sales_data_simulate_create_new(self):
        # simple test of product creation
        all_product_count = Product.objects.all().count()
        with mock.patch('requests.get', side_effect=self.mocked_requests_get):
            response = self.client.get(self.url_update_sales_records)
            new_product_count = Product.objects.all().count()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertNotEqual(all_product_count, new_product_count)
            self.assertEqual(new_product_count, 1)

    def test_past_product_record_creation(self):
        # don't create past record if the price is the same.
        existing_product = Product.objects.create(
            name=self.mock_data['product_records'][0]['name'],
            price_in_pennies=int(round(float(self.mock_data['product_records'][0]['price'].strip('$'))*100)),
            external_product_id=self.mock_data['product_records'][0]['id']
        )
        past_records_count = PastPriceRecord.objects.all().count()
        with mock.patch('requests.get', side_effect=self.mocked_requests_get):
            response = self.client.get(self.url_update_sales_records)
            new_past_record_count = PastPriceRecord.objects.all().count()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(past_records_count, new_past_record_count)

            # change price of existing product, now a past record will be created
            existing_product.price_in_pennies = 3525
            existing_product.save()
            response = self.client.get(self.url_update_sales_records)
            new_past_record_count = PastPriceRecord.objects.all().count()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertNotEqual(past_records_count, new_past_record_count)

    def test_product_mismatch(self):
        Product.objects.create(
            name="some_mismatched_name",
            price_in_pennies=int(round(float(self.mock_data['product_records'][0]['price'].strip('$'))*100)),
            external_product_id=self.mock_data['product_records'][0]['id']
        )
        with self.assertRaises(Exception) as context:
            with mock.patch('requests.get', side_effect=self.mocked_requests_get):
                response = self.client.get(self.url_update_sales_records)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue('does not match external product name' in context.exception)
