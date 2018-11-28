from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import time
from datetime import date
import serial
from apps.proveedor.models import Proveedor, Control, Puesto
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
	
	if codigo=='82 CD CD 73':
		return redirect('proveedor:home')

	elif existencia:
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
	'''if request.is_ajax():
		idEliminar = request.POST.get('inputEliminar')
		proveedor_e = Proveedor.objects.filter(id =idEliminar).exists()
		if proveedor_e:
			proveedor = Proveedor.objects.get(id =idEliminar)
			proveedor.delete()
			return redirect('proveedor:adm_proveedor')'''
	if request.method == 'POST':
		if 'inputEliminar' in request.POST:
			idEliminar = request.POST.get('inputEliminar')
			proveedor_e = Proveedor.objects.filter(id =idEliminar).exists()
			if proveedor_e:
				proveedor = Proveedor.objects.get(id =idEliminar)
				proveedor.delete()
				return redirect('proveedor:adm_proveedor')
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

def puestos_lista(request):
	puestos = Puesto.objects.all()
	return render(request, 'puesto/puestos_lista.html', {'puestos':puestos})

def editar_puesto(request, id_puesto):
	puesto = Puesto.objects.get(id = id_puesto)
	if request.method == 'GET':
		form = PuestoForm(instance = puesto)
	else:
		form = PuestoForm(request.POST, request.FILES or None, instance=puesto)
		if form.is_valid():
			form.save()
			pass
		return redirect('proveedor:puestos_lista')
	return render(request, 'puesto/puesto_editar.html', {'form':form,'puesto':puesto})

def eliminar_puesto(request, id_puesto):
	puesto = Puesto.objects.get(id = id_puesto)
	if 'btnEliminar' in request.POST:
		id_puesto = request.POST['id_puesto']
		puesto = Puesto.objects.get(id = id_puesto)
		puesto.delete()
		return redirect('proveedor:puestos_lista')
		pass
	return render(request,'puesto/eliminar_puesto.html', {'puesto':puesto})

def historial(request):
	controles = Control.objects.all()
	if 'btnBuscar' in request.GET:
		if request.GET['txtNombre'] != "" and request.GET['txtFechaInicial'] == "":
			nombre_proveedor = request.GET['txtNombre']
			proveedor = Proveedor.objects.get(nombre_proveedor__contains = nombre_proveedor)
			controles = Control.objects.filter(proveedor = proveedor)
			pass

		elif request.GET['txtNombre'] == "" and request.GET['txtFechaInicial'] != "":
			fecha_inicio = request.GET['txtFechaInicial']
			fecha_final = request.GET['txtFechaFinal']
			controles = Control.objects.filter(fecha_entrada__range=(fecha_inicio,fecha_final))
			pass
			
		elif request.GET['txtNombre'] != "" and request.GET['txtFechaInicial'] != "":
			fecha_inicio = request.GET['txtFechaInicial']
			fecha_final = request.GET['txtFechaFinal']
			nombre_proveedor = request.GET['txtNombre']
			proveedor = Proveedor.objects.get(nombre_proveedor__contains = nombre_proveedor)
			controles = Control.objects.filter(proveedor = proveedor).filter(fecha_entrada__range=(fecha_inicio,fecha_final))
			pass
		pass

	return render(request, 'proveedor/historial.html', {'controles':controles})

def crear_puesto(request):
	if request.method == 'POST':
		form = PuestoForm(request.POST)
		if form.is_valid():
			form.save()
			pass
		return redirect('proveedor:puestos_lista')
	else:
		form = PuestoForm()
	return render(request, 'puesto/crear_puesto.html', {'form':form})

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

def capcu2(request):
	return render(request, 'proveedor/capturar_codigo.html')

def home(request):
	return render(request, 'base/index.html')

def captura(request):
	codigo=lectura(request)
	mensaje=''

	codigo=codigo.decode('utf-8')
	codigo=codigo[1:12]

	existencia = Proveedor.objects.filter(codigo_proveedor=codigo).exists()
	if existencia:
		mensaje = 'Ya se encuentra registrado un proveedor con el codigo: '+codigo+', '+'Intente con una nueva tarjeta'
	else:
		mensaje = 'El codigo de la tarjeta es: '+codigo+', '+'¿Desea Registrarlo?'



	context={
		'mensaje': mensaje,
		'existencia': existencia,
		'codigo': codigo,
	}
	return render(request, 'proveedor/pre_crear.html', context)