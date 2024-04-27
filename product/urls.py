from django.urls import include, path
from .json import (shop_data, get_random_products, load_special_products)
from cart.payment import fadax_pay

urlpatterns = [
    path('shop_data', shop_data),
    path('fadax', fadax_pay),
    path('get_random_products', get_random_products),
    path('load_special_products', load_special_products),
]