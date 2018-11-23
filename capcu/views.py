from django.shortcuts import render
from django.http import HttpResponse
import time
import serial

	
	
def base(request):
    return render (request, 'base/base.html')

def componentes(request):
    return render (request, 'componentes.html' )

def login(request):
    return render (request, 'login/login.html' )

def prueba(request):
	arduino = serial.Serial('COM4', 9600)
	prueba=''

	while prueba == '':
		prueba = arduino.readline()
	arduino.close()
	return HttpResponse(prueba)