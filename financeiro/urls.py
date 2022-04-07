from django.contrib import admin
from django.urls import path

from movimentacao.endpoints.forma_pagamento_rest import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
