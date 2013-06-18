# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from pizzadb.models import Pizza, Skladnik, PizzaKlienta, Zamowienie
from django.shortcuts import render
from django.contrib.auth import authenticate, login

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
		return render(request, 'logowanie.html$powrot=%s' % request.path )
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

def mojepizze(request):
	if(request.user.is_anonymous()):
		return render(request, 'logowanie.html')
	pizze = PizzaKlienta.objects.filter(klient=request.user)
	return render(request, 'mojepizze.html', { 'pizze' : pizze } )

def logowanie( request ):
	
	try:
		powrot = request.GET['powrot']
	except ( KeyError ):
		return render( request, 'logowanie.html', { 'powrot' : reverse(menu) } )
	else: 
		return render( request, 'logowanie.html', { 'powrot' : powrot } )

def log( request ):
	try:
		nazwa = request.POST['login']
		haslo = request.POST['haslo']
		powrot = request.POST['powrot']
	except ( KeyError ):
		return render ( request, 'logowanie.html' )
	else:
<<<<<<< HEAD
		uzytkownik = authenticate( username=nazwa, password=haslo )
		if uzytkownik is not None:
			if uzytkownik.is_active:
				login( request, uzytkownik )
				return HttpResponseRedirect( powrot )
			else:
				return render( request, 'logowanie.html', { 'blad' : "Konto jest nieaktywne" } )
		else:
			return render( request, 'logowanie.html', { 'blad' : "Dane niepoprawne" } )
=======
		return HttpResponse( "Nie ma takiego" )

def obsluga(request):
	# a co jesli nie jestem pracownikiem?
	if(request.user.is_anonymous()):
		return render(request, 'logowanie.html')
	moje_zamowienia = Zamowienie.objects.filter(pracownik=request.user)
	wolne_zamowienia = Zamowienie.objects.filter(pracownik__isnull=True)
	return render( request, 'obsluga.html', { 'moje' : moje_zamowienia, 'wolne' : wolne_zamowienia } )	
	
>>>>>>> e9f8e97c255691ae50cccffcf87daf6fc2bfa0c9
