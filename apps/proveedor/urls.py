from django.contrib import admin
from django.urls import path
from apps.proveedor.views import *

urlpatterns = [
    path( '', view_proveedor, name="view_proveedor"),
]
