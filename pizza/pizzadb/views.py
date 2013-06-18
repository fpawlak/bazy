#Create your views here.

from django.http import HttpResponse
from pizzadb.models import Pizza
from django.shortcuts import render
from django.contrib.auth import authenticate, login

def index( request ):
	return HttpResponse( "LOL jakie to jest zjebane." )

def menu( request ):
	p = Pizza.objects.all()
	return render( request, 'menu.html', { 'list' : p } )

def logowanie( request ):
	return render( request, 'logowanie.html' )

def log( request ):
	nazwa = request.POST['login']
	haslo = request.POST['haslo']
	uzytkownik = authenticate( username=nazwa, password=haslo )
	if uzytkownik is not None:
		if uzytkownik.is_active:
			login( request, uzytkownik )
			return HttpResponse( "JEST" )
		else:
			return HttpResponse( "BAN!!!" )
	else:
		return HttpResponse( "Nie ma takiego" )
