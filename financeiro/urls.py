from django.contrib import admin
from django.urls import path

from movimentacao.endpoints.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

