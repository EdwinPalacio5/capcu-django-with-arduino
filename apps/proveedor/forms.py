from django import forms
from apps.proveedor.models import *

class ProveedorForm(forms.ModelForm):

	class Meta:
		model = Proveedor
		fields = [
			'nombre_proveedor',
			'categoria_proveedor',
			'puesto_proveedor',
		]
		labels = {
			'nombre_proveedor':'Nombre de Proveedor:',
			'categoria_proveedor':'Categorias de Producto:',
			'puesto_proveedor':'Puestos que abastece:',
		}
		widgets = {
			'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre del proveedor'}),
			'categoria_proveedor':forms.CheckboxSelectMultiple(),
			'puesto_proveedor':forms.CheckboxSelectMultiple(),
		}

class PuestoForm(forms.ModelForm):

	class Meta:
		model = Puesto
		fields = [
			'nombre_puesto',
			'representante_puesto',
			'ubicacion_puesto',
			'categoria_puesto',
		]
		labels = {
			'nombre_puesto':'Nombre del puesto:',
			'representante_puesto':'Representante del puesto:',
			'ubicacion_puesto':'Ubicacion del puesto:',
			'categoria_puesto':'Categorias del puesto:',
		}
		widgets = {
			'nombre_puesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre del puesto'}),
			'representante_puesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre del representante del puesto'}),
			'ubicacion_puesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ubicacion exacta del puesto'}),
			'categoria_puesto': forms.CheckboxSelectMultiple(),
		}
