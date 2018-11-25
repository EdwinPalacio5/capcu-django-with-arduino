from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import time
from datetime import date
import serial
from apps.proveedor.models import Proveedor, Control
from apps.proveedor.forms import *

# Create your views here.
def capcu(request):
	return render(request, 'proveedor/capcu.html')

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

def lectura(request):
	arduino = serial.Serial('COM4', 9600)
	codigo=''
	while codigo == '':
		codigo = arduino.readline()
	arduino.close()

	return codigo

def proveedor_mostrar(request):
	codigo=lectura(request)
	mensaje=''
	proveedor=''
	control=''
	ingreso_salida=''
	hora_ingreso=time.strftime("%H:%M:%S")

	codigo=codigo.decode('utf-8')
	codigo=codigo[1:12]

	existencia = Proveedor.objects.filter(codigo_proveedor=codigo).exists()
	if existencia:
		proveedor = Proveedor.objects.get(codigo_proveedor=codigo)
		if not proveedor.estado_control:
			entrada(request, proveedor)
			control='Entrada'
			ingreso_salida='Hora de ingreso'
		else:
			salida(request, proveedor)
			control='Salida'
			ingreso_salida='Hora de salida'

	else:
		mensaje = 'No se encontró ningun proveedor con el codigo: '+codigo+', '+'¿Desea Registrarlo?'



	context={
		'proveedor': proveedor,
		'mensaje': mensaje,
		'existencia': existencia,
		'hora_ingreso': hora_ingreso,
		'control': control,
		'ingreso_salida':ingreso_salida,
	}
	return render(request, 'proveedor/proveedor_mostrar.html', context)

def proveedores_dentro(request):
	proveedores = Control.objects.filter(control=True)
	return render(request, 'proveedor/proveedores_dentro.html', {'proveedores':proveedores})
'''
def ajax(request):
	arduino = serial.Serial('COM4', 9600, timeout=2)
	codigo=''
	mensaje=''
	proveedor=''
	control=''
	ingreso_salida=''
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
			ingreso_salida='Hora de ingreso'
		else:
			salida(request, proveedor)
			control='Salida'
			ingreso_salida='Hora de salida'

	else:
		mensaje = 'No hay proveedores con el codigo: '+codigo+', '+'¿Desea Registrarlo?'

	context={
		'proveedor': proveedor,
		'mensaje': mensaje,
		'existencia': existencia,
		'hora_ingreso': hora_ingreso,
		'control': control,
		'ingreso_salida':ingreso_salida,
	}
	return render(request, 'proveedor/ajax.html', context)
'''


def adm_proveedor(request):
	lista_proveedores = list()
	lista_interna = list()
	if request.is_ajax():
		idEliminar = request.POST.get('inputEliminar')
		proveedor_e = Proveedor.objects.filter(id =idEliminar).exists()
		if proveedor_e:
			proveedor = Proveedor.objects.get(id =idEliminar)
			proveedor.delete()
			return redirect('proveedor:adm_proveedor')
	if request.method == 'POST':
		if 'btnEditar' in request.POST:
			id_editar = request.POST.get('inputEditar')
			proveedor_el = Proveedor.objects.filter(id = id_editar).exists()
			if proveedor_el:
				proveedor = Proveedor.objects.get(id = id_editar)
				form_proveedor = ProveedorForm(request.POST, instance= proveedor)
				if form_proveedor.is_valid():
					form_proveedor.save()
					return redirect('proveedor:adm_proveedor')

	proveedores = Proveedor.objects.all()
	for proveedor in proveedores:
		form = ProveedorForm(instance=proveedor)
		lista_interna.append(proveedor)
		lista_interna.append(form)
		lista_proveedores.append(lista_interna)
		lista_interna=[]

	return render(request, 'proveedor/listar_proveedores.html', {'proveedores': lista_proveedores})

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
