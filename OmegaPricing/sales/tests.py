import mock
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status


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

    def test_get_sales_data(self):
        with mock.patch('requests.get', side_effect=self.mocked_requests_get):
            response = self.client.get(self.url_update_sales_records)
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
