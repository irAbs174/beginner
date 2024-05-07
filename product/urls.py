from django.urls import include, path
from .json import (search, single_product_data, shop_data, get_random_products,load_special_products, load_category_items, load_brand_items)
from cart.payment import fadax_pay
from index.views import submit_comment

urlpatterns = [
    path('search', search),
    path('single_product_data', single_product_data),
    path('shop_data', shop_data),
    path('submit_comment', submit_comment),
    path('fadax', fadax_pay),
    path('get_random_products', get_random_products),
    path('load_special_products', load_special_products),
    path('load_category_items', load_category_items),
    path('load_brand_items', load_brand_items),
]