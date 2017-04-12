# from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.


class SalesTests(APITestCase):

    def test_sales_create(self):
        # initial test to to make sure docker
        # and project are set up correctly.
        self.assertEqual(True, True)
