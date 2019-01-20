from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import time
from datetime import date, datetime
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
	time.sleep(2)
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
	
	if codigo=='90 4D 32 5C':
		arduino = serial.Serial('COM4', 9600)
		time.sleep(2)
		arduino.write(b'a')
		time.sleep(2)
		arduino.close()
		return redirect('proveedor:home')

	elif existencia:
		arduino = serial.Serial('COM4', 9600)
		time.sleep(2)
		arduino.write(b'a')
		time.sleep(1)
		arduino.close()
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
		arduino = serial.Serial('COM4', 9600)
		time.sleep(2)
		arduino.write(b'b')
		time.sleep(1)
		arduino.close()
		mensaje = 'No se encontró ningun proveedor con el codigo: '+codigo+', '+'Consulte con el administrador para registrarla'



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
	for x in puestos:
		if 'btnEliminarPuesto' + str(x.id) in request.POST:
			puesto = Puesto.objects.get(id = x.id)
			puesto.delete()
			return redirect('proveedor:puestos_lista')
			pass
		pass
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
	contexto = {}
	no_controles = "¡No se encontro ningún registro con los parametros recibidos!"
	faltan_parametros = "Parametros insuficientes para realizar el filtro de controles."
	if not request.user.is_authenticated:
		controles = Control.objects.filter(fecha_entrada = date.today())
		pass
	else:
		controles = Control.objects.all()

	

	contexto = {'controles':controles, 'no_controles':""}

	if 'btnBuscar' in request.GET:
		controles = []
		if request.GET['txtNombre'] != "" and request.GET['txtFechaInicial'] == "" and request.GET['txtFechaFinal'] == "":
			nombre_proveedor = request.GET['txtNombre']
			if Proveedor.objects.filter(nombre_proveedor__contains = nombre_proveedor).exists():
				proveedores = Proveedor.objects.filter(nombre_proveedor__contains = nombre_proveedor)
				for proveedor in proveedores:
					controles_filtrados = Control.objects.filter(proveedor = proveedor)
					for control in controles_filtrados:
						controles.append(control)
						pass
					pass
				contexto = {'controles':controles, 'no_controles':""}
				pass
			else:
				contexto = {'controles':[],'no_controles':no_controles}
				pass
			pass

		elif request.GET['txtNombre'] == "" and request.GET['txtFechaInicial'] != "" and request.GET['txtFechaFinal'] != "":
			fecha_inicio = request.GET['txtFechaInicial']
			fecha_final = request.GET['txtFechaFinal']
			controles = Control.objects.filter(fecha_entrada__range=(fecha_inicio,fecha_final))

			if controles.count() == 0:
				contexto = {'controles':[], 'no_controles':no_controles}
				pass
			else:
				contexto = {'controles':controles, 'no_controles':""}
				pass
			pass
			
		elif request.GET['txtNombre'] != "" and request.GET['txtFechaInicial'] != "" and request.GET['txtFechaFinal'] != "":
			fecha_inicio = request.GET['txtFechaInicial']
			fecha_final = request.GET['txtFechaFinal']
			nombre_proveedor = request.GET['txtNombre']

			if Proveedor.objects.filter(nombre_proveedor__contains = nombre_proveedor).exists():
				proveedores_filtrados = Proveedor.objects.filter(nombre_proveedor__contains = nombre_proveedor)
				for proveedor in proveedores_filtrados:
					controles_filtrados = Control.objects.filter(proveedor = proveedor).filter(fecha_entrada__range=(fecha_inicio,fecha_final))
					for control in controles_filtrados:
						controles.append(control)
						pass
					pass
				pass

			if controles == []:
				contexto = {'controles':[], 'no_controles':no_controles}
				pass
			else:
				contexto = {'controles':controles, 'no_controles':""}
				pass
			pass

		else:
			contexto = {'controles':[], 'no_controles':"", 'faltan_parametros':faltan_parametros}
			pass
		pass
		
	tiempos = []
	if controles != []:
		for control in controles:
			tiempos.append(datetime.combine(date.today(), control.hora_salida) - datetime.combine(date.today(), control.hora_entrada))
			pass
		contexto['tiempos'] = tiempos
		controles_tiempos = zip(contexto['controles'], contexto['tiempos'])
		contexto['controles_tiempos'] = controles_tiempos
		pass

	return render(request, 'proveedor/historial.html', contexto)

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