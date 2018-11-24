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