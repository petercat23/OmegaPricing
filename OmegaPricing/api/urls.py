from django.conf.urls import url
from . import sales_api

urlpatterns = [
    url(r'^products/update/?$', sales_api.GetUpdatedSalesRecords.as_view(), name='updateSales'),
]
