from django.shortcuts import render
from django.http import HttpResponse
import time
from datetime import date
import serial
from apps.proveedor.models import Proveedor, Control

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


