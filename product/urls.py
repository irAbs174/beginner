from django.urls import include, path
from .json import (search, shop_data, get_random_products,load_special_products, load_category_items, load_brand_items)
from cart.payment import fadax_pay

urlpatterns = [
    path('search', search),
    path('shop_data', shop_data),
    path('fadax', fadax_pay),
    path('get_random_products', get_random_products),
    path('load_special_products', load_special_products),
    path('load_category_items', load_category_items),
    path('load_brand_items', load_brand_items),
]