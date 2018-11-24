from django.shortcuts import render, redirect
from django.http import HttpResponse
import time
from datetime import date
import serial
from apps.proveedor.models import Proveedor, Control
from apps.proveedor.forms import *

# Create your views here.
def proveedor_show(request):
	'''arduino = serial.Serial('COM4', 9600)
				codigo=''
				mensaje=''
				proveedor=''
				hora_ingreso=time.strftime("%H:%M:%S")
				
				while codigo == '':
					codigo = arduino.readline()
				arduino.close()
			
				codigo=codigo.decode('utf-8')
				codigo=codigo[1:12]
			
				existencia = Proveedor.objects.filter(codigo_proveedor='82 CD CD 73').exists()
				if existencia:
					proveedor = Proveedor.objects.get(codigo_proveedor='82 CD CD 73')
				else:
					mensaje = 'No hay proveedores con el codigo: '+codigo+', '+'¿Desea Registrarlo?'
			
				context={
					'proveedor': proveedor,
					'mensaje': mensaje,
					'existencia': existencia,
					'hora_ingreso':hora_ingreso,
				}'''
	return render(request, 'proveedor/proveedor_show.html')

def entrada(request, proveedor):
	proveedor.estado_control=True
	control = Control()
	control.fecha_entrada=date.today()
	control.hora_entrada=time.strftime("%H:%M:%S")
	control.proveedor=proveedor
	control.save()
	proveedor.save()
			
def salida(request, proveedor):
	control = Control.objects.filter(proveedor=proveedor.id).latest('id')
	control.fecha_salida=date.today()
	control.hora_salida=time.strftime("%H:%M:%S")
	control.control=False
	proveedor.estado_control=False
	control.save()
	proveedor.save()

def ajax(request):
	arduino = serial.Serial('COM4', 9600)
	codigo=''
	mensaje=''
	proveedor=''
	control=''
	hora_ingreso=time.strftime("%H:%M:%S")

	while codigo == '':
		codigo = arduino.readline()
	arduino.close()

	codigo=codigo.decode('utf-8')
	codigo=codigo[1:12]

	existencia = Proveedor.objects.filter(codigo_proveedor=codigo).exists()
	if existencia:
		proveedor = Proveedor.objects.get(codigo_proveedor=codigo)
		if not proveedor.estado_control:
			entrada(request, proveedor)
			control='Entrada'
		else:
			salida(request, proveedor)
			control='Salida'

	else:
		mensaje = 'No hay proveedores con el codigo: '+codigo+', '+'¿Desea Registrarlo?'

	context={
		'proveedor': proveedor,
		'mensaje': mensaje,
		'existencia': existencia,
		'hora_ingreso': hora_ingreso,
		'control': control,
	}
	return render(request, 'proveedor/ajax.html', context)

def proveedores_dentro(request):
	proveedores = Control.objects.filter(control=True)
	return render(request, 'proveedor/proveedores_dentro.html', {'proveedores':proveedores})

def adm_proveedor(request):
	proveedores = Proveedor.objects.all()
	return render(request, 'proveedor/listar_proveedores.html', {'proveedores':proveedores})

def crear_proveedor(request,codigo):
	if request.method == 'POST':
		if 'btnForm1' in request.POST:
			form_proveedor =  ProveedorForm(request.POST, request.FILES or None)
			if form_proveedor.is_valid():
				proveedor2 = form_proveedor.save(commit=False)
				proveedor2.codigo_proveedor = codigo
				proveedor2.save()
				form_proveedor.save_m2m()
				return redirect('proveedor:adm_proveedor')
	else:
		form_proveedor = ProveedorForm()
	proveedores = Proveedor.objects.all()
	return render(request, 'proveedor/crear_proveedor.html', {'form_proveedor':form_proveedor,'codigo':codigo})


def editar_proveedor(request, id):
	proveedor = Proveedor.objects.get(id=id)
	if request.method == 'GET':
		form = ProveedorForm(instance=proveedor)
	else:
		form = ProveedorForm(request.POST, request.FILES or None, instance=proveedor)
		if form.is_valid():
			form.save()
		return redirect('proveedor:adm_proveedor')
	return render(request, 'proveedor/editar_proveedor.html', {'form_proveedor':form, 'proveedor':proveedor,},)
