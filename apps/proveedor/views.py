from django.shortcuts import render
from django.http import HttpResponse
import time
from datetime import date
import serial
from apps.proveedor.models import Proveedor, Control

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

