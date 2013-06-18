# Create your views here.

from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
<<<<<<< HEAD
from pizzadb.models import Pizza, Skladnik, PizzaKlienta, Zamowienie, User
=======
from pizzadb.models import Pizza, Skladnik, PizzaKlienta, Zamowienie, Zamowienie_Pizza, Zamowienie_PizzaKlienta, Zamowienie_Dodatek, Dodatek
>>>>>>> d15cab7954e7b4bc4275fcbba533f2aaf0d55fb6
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def index( request ):
	return HttpResponse( "LOL jakie to jest zjebane." )

def menu( request ):
	p = Pizza.objects.all()
	if request.user.is_authenticated():
		return render( request, 'menu.html', { 'list' : p, 'zalogowany' : 'asdasd' } )
	else:
		return render( request, 'menu.html', { 'list' : p } )

# def order(request):
# 	menu = Pizza.objects.all()
# 	return render(request, 'order.html', { 'menu' : menu })

def wlasnapizza(request):
	skladniki = Skladnik.objects.all()
	return render(request, 'wlasnapizza.html', { 'skladniki' : skladniki } )

def dodajpizze(request):
	if(request.user.is_anonymous()):
		return redirect('/logowanie/?powrot=%s' % request.path )
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
		return redirect( '/logowanie/?powrot=%s' % request.path )
	pizze = PizzaKlienta.objects.filter(klient=request.user)
	return render(request, 'mojepizze.html', { 'pizze' : pizze } )

def logowanie( request ):
	
	try:
		powrot = request.GET['powrot']
	except ( KeyError ):
		return render( request, 'logowanie.html', { 'powrot' : reverse(menu) } )
	else: 
		return render( request, 'logowanie.html', { 'powrot' : powrot } )

def wyloguj( request ):
	logout( request )
	return HttpResponseRedirect(reverse(menu))

def rejestracja( request ):
	return render( request, 'rejestracja.html' )

def log( request ):
	try:
		nazwa = request.POST['login']
		haslo = request.POST['haslo']
		powrot = request.POST['powrot']
	except ( KeyError ):
		return render ( request, 'logowanie.html' )
	else:
		uzytkownik = authenticate( username=nazwa, password=haslo )
		if uzytkownik is not None:
			if uzytkownik.is_active:
				login( request, uzytkownik )
				return HttpResponseRedirect( powrot )
			else:
				return render( request, 'logowanie.html', { 'blad' : "Konto jest nieaktywne" } )
		else:
			return render( request, 'logowanie.html', { 'blad' : "Dane niepoprawne" } )

def obsluga(request):
	# a co jesli nie jestem pracownikiem?
	if(request.user.is_anonymous()):
		return redirect( '/logowanie/?powrot=%s' % request.path )
	moje_zamowienia = Zamowienie.objects.filter(pracownik=request.user)
	wolne_zamowienia = Zamowienie.objects.filter(pracownik__isnull=True)
	return render( request, 'obsluga.html', { 'moje' : moje_zamowienia, 'wolne' : wolne_zamowienia } )

def zamowienie(request):
	menu = Pizza.objects.all()
	custom = PizzaKlienta.objects.filter(klient=request.user)
	dodatki = Dodatek.objects.all()
	return render(request, 'zamowienie.html', { 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki })


def zlozzamowienie(request):
	menu = Pizza.objects.all()
	custom = PizzaKlienta.objects.filter(klient=request.user)
	dodatki = Dodatek.objects.all()

	# sprawdzamy, czy ilosci sa wartosciami liczbowymi i  czy nie
	# sumuja sie do zera

	laczna_ilosc = 0
	
	for pizza in menu:
		try:
			laczna_ilosc += int(request.POST['menu' + str(pizza.id)])
		except:
			return render(request, 'zamowienie.html', { 'error_message' : "Musisz podac wartosci liczbowe!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki })

	for pizza in custom:
		try:
			laczna_ilosc += int(request.POST['custom' + str(pizza.id)])
		except:
			return render(request, 'zamowienie.html', { 'error_message' : "Musisz podac wartosci liczbowe!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki })

	for dodatek in dodatki:
		try:
			laczna_ilosc += int(request.POST['dodatek' + str(dodatek.id)])
		except:
			return render(request, 'zamowienie.html', { 'error_message' : "Musisz podac wartosci liczbowe!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki })
		
	if laczna_ilosc == 0:
		return render(request, 'zamowienie.html', { 'error_message' : "Musisz cos zamowic!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki })
		
	nowe_zamowienie = Zamowienie(
		klient = request.user,
		data = date.today(),
		platnoscKarta = ("platnoscKarta" in request.POST.keys()),
		telefon = request.POST['telefon'],
		adres = request.POST['adres'],
		dostarczono = False)
	nowe_zamowienie.kwota = 0
	nowe_zamowienie.save()
	


	for pizza in menu:
		ilosc = int(request.POST['menu' + str(pizza.id)])
		zamowienie_pizza = Zamowienie_Pizza(
			zamowienie = nowe_zamowienie,
			pizza = pizza,
			ilosc = ilosc)
		zamowienie_pizza.save()
		nowe_zamowienie.kwota += pizza.cena * ilosc

	for pizza in custom:
		ilosc = int(request.POST['custom' + str(pizza.id)])
		zamowienie_pizzaklienta = Zamowienie_PizzaKlienta(
			zamowienie = nowe_zamowienie,
			pizzaKlienta = pizza,
			ilosc = ilosc)
		zamowienie_pizzaklienta.save()
		nowe_zamowienie.kwota += pizza.cena * ilosc

			
	for dodatek in dodatki:
		ilosc = int(request.POST['dodatek' + str(dodatek.id)])
		zamowienie_dodatek = Zamowienie_Dodatek(
			zamowienie = nowe_zamowienie,
			dodatek = dodatek,
			ilosc = ilosc)
		zamowienie_dodatek.save()
		nowe_zamowienie.kwota += dodatek.cena * ilosc

	nowe_zamowienie.save()
	return HttpResponseRedirect("../menu/")
