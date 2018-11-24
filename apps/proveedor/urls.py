from django.contrib import admin
from django.urls import path
from apps.proveedor import views

app_name="proveedor"

urlpatterns = [
    path('', views.capcu, name="mostrar"),
    path('mostrar/', views.proveedor_mostrar, name="mostrar"),
    path('dentro/', views.proveedores_dentro, name="dentro"),
]
