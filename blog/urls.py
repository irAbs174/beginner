from django.urls import path
from .api import (blog_archive_data,)


urlpatterns = [
    path('archive_data', blog_archive_data),
]