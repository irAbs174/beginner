from django.urls import include, path
from .json import (shop_data, get_2_random_products)
from cart.payment import fadax_pay

urlpatterns = [
    path('shop_data', shop_data),
    path('fadax', fadax_pay),
    path('get_2_random_products', get_2_random_products),
]