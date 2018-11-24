from django.contrib import admin
from django.urls import path
from apps.proveedor import views

app_name="proveedor"

urlpatterns = [
    path('mostrar/', views.proveedor_show, name="mostrar"),
    path('ajax/', views.ajax, name="ajax"),
    path('dentro/', views.proveedores_dentro, name="dentro"),
    path('administrar-proveedores/',views.adm_proveedor , name="adm_proveedor"),
    path('nuevo-proveedor/<codigo>/', views.crear_proveedor, name="crear_proveedor"),
    path('editar-proveedor/<id>/', views.editar_proveedor,name="editar_proveedor")

]
