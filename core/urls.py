from django.contrib import admin
from django.urls import path

from core.api import api

urlpatterns = [
    path("api/v1/", api.urls),
    path("", admin.site.urls)
]
