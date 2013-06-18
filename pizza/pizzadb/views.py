# Create your views here.

from django.http import HttpResponse
from pizzadb.models import Pizza
from django.shortcuts import render

def index( request ):
	return HttpResponse( "LOL jakie to jest zjebane." )

def menu( request ):
	p = Pizza.objects.all()
	return render( request, 'menu.html', { 'list' : p } )
