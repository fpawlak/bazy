# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from pizzadb.models import Pizza, Skladnik, PizzaKlienta
from django.shortcuts import render

def index( request ):
	return HttpResponse( "LOL jakie to jest zjebane." )

def menu( request ):
	p = Pizza.objects.all()
	return render( request, 'menu.html', { 'list' : p } )

# def order(request):
# 	menu = Pizza.objects.all()
# 	return render(request, 'order.html', { 'menu' : menu })

def wlasnapizza(request):
	skladniki = Skladnik.objects.all()
	return render(request, 'wlasnapizza.html', { 'skladniki' : skladniki } )

def dodajpizze(request):
	if(request.user.is_anonymous()):
		return render(request, 'logowanie.html')
	nazwa_pizzy = request.POST['NazwaPizzy']
	skladniki = []
	cena = 0
	for skladnik in Skladnik.objects.all():
		if str(skladnik.id) in request.POST.keys(): # skladnik zostal zaznaczony
			skladniki.append(skladnik)
			cena += skladnik.cena
	nowa_pizza = PizzaKlienta(nazwa = nazwa_pizzy, klient = request.user, cena = cena)
	nowa_pizza.save()
	for skladnik in skladniki:
		nowa_pizza.skladniki.add(skladnik)
	return HttpResponseRedirect(reverse(menu))
