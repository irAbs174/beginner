from django.urls import include, path
from .json import (shop_data)

urlpatterns = [
    path('shop_data', shop_data),
]