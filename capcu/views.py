from django.shortcuts import render
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


	
	
def base(request):
    return render (request, 'base/base.html')

def componentes(request):
    return render (request, 'componentes.html' )

def login(request):
    return render (request, 'login/login.html' )