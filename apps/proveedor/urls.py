from django.contrib import admin
from django.urls import path
from apps.proveedor import views

app_name="proveedor"

urlpatterns = [
    path('', views.capcu, name="mostrar"),
    path('mostrar/', views.proveedor_mostrar, name="mostrar"),
    path('dentro/', views.proveedores_dentro, name="dentro"),
    path('administrar-proveedores/',views.adm_proveedor , name="adm_proveedor"),
    path('nuevo-proveedor/<codigo>/', views.crear_proveedor, name="crear_proveedor"),
    path('editar-proveedor/<id>/', views.editar_proveedor,name="editar_proveedor"),
    path('puestos-lista/', views.puestos_lista ,name="puestos_lista"),
	path('nuevo-puesto/', views.crear_puesto ,name="crear_puesto"),
	path('editar-puesto/<id_puesto>/', views.editar_puesto,name="editar_puesto"),
	path('eliminar-puesto/<id_puesto>/', views.eliminar_puesto,name="eliminar_puesto"),
    path('historial/', views.historial,name="historial"),
]
