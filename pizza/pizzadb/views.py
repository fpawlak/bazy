# Create your views here.
# -*- coding: utf-8 -*-

from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from pizzadb.models import Pizza, Skladnik, PizzaKlienta, Zamowienie, User, Uzytkownik
from pizzadb.models import Pizza, Skladnik, PizzaKlienta, Zamowienie, Zamowienie_Pizza, Zamowienie_PizzaKlienta, Zamowienie_Dodatek, Dodatek
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def index( request ):
	return HttpResponse( "LOL jakie to jest zjebane." )

def menu( request ):
	p = Pizza.objects.all()
	napoje = Dodatek.objects.all().filter( rodzaj = 'n' )
	sosy = Dodatek.objects.all().filter( rodzaj = 's' )
	salatki = Dodatek.objects.all().filter( rodzaj = 'j' )
	if request.user.is_authenticated():
		return render( request, 'menu.html', { 'pizze' : p, 'zalogowany' : 't', 'napoje' : napoje, 'sosy' : sosy, 'salatki' : salatki } )
	else:
		return render( request, 'menu.html', { 'pizze' : p, 'napoje' : napoje, 'sosy' : sosy, 'salatki' : salatki } )

# def order(request):
# 	menu = Pizza.objects.all()
# 	return render(request, 'order.html', { 'menu' : menu })

def wlasnapizza(request):
	if(request.user.is_anonymous()):
		return redirect('/logowanie/?powrot=%s' % request.path )
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
	return HttpResponseRedirect(reverse(mojepizze))

def mojepizze(request):
	if(request.user.is_anonymous()):
		return redirect( '/logowanie/?powrot=%s' % request.path )
	pizze = PizzaKlienta.objects.filter(klient=request.user)
	return render(request, 'mojepizze.html', { 'pizze' : pizze } )

def logowanie( request ):
	
	zalogowany = 't' if request.user.is_authenticated() else 'f'
	
	try:
		powrot = request.GET['powrot']
	except ( KeyError ):
		return render( request, 'logowanie.html', { 'powrot' : reverse(menu), 'zalogowany' : zalogowany } )
	else: 
		return render( request, 'logowanie.html', { 'powrot' : powrot, 'zalogowany' : zalogowany  } )


def wyloguj( request ):
	
	logout( request )
	return HttpResponseRedirect( reverse(menu) )

def rejestracja( request ):
	return render( request, 'rejestracja.html' )

def rejestruj( request ):
	try:
		nazwa = request.POST['nazwa']
		haslo = request.POST['haslo']
		haslo2 = request.POST['haslo2']
		imie = request.POST['imie']
		nazwisko = request.POST['nazwisko']
		adres = request.POST['adres']
		telefon = request.POST['telefon']
		email = request.POST['email']
	except:
		return render( request, 'rejestracja.html', { 'blad' : "Niepoprawne dane" } )
	else:
		if haslo != haslo2:
			return render( request, 'rejestracja.html', { 'blad' : "Niepoprawne dane" } )
		else:
			try:
				ktos = User.objects.get( username = nazwa )
			except( User.DoesNotExist ):
				user = User.objects.create_user( username = nazwa, password = haslo )
				uzytkownik = Uzytkownik( imie = imie, nazwisko = nazwisko, adres = adres, telefon = telefon, funkcja = 'u', email = email, usrId = user )
				user.save()
				uzytkownik.save()
				return redirect( '/logowanie/' )
			else:
				return render( request, 'rejestracja.html', { 'blad' : "Nazwa zajęta" } )


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
				return redirect( powrot )
			else:
				return render( request, 'logowanie.html', { 'blad' : "Konto jest nieaktywne" } )
		else:
			return render( request, 'logowanie.html', { 'blad' : "Dane niepoprawne" } )

def obsluga(request):
	# a co jesli nie jestem pracownikiem?
	if(request.user.is_anonymous()):
		return redirect( '/logowanie/?powrot=%s' % request.path )
	moje_zamowienia = Zamowienie.objects.filter(pracownik=request.user, dostarczono=False).order_by('-data')
	wolne_zamowienia = Zamowienie.objects.filter(pracownik__isnull=True).order_by('-data')
	return render( request, 'obsluga.html', { 'moje' : moje_zamowienia, 'wolne' : wolne_zamowienia } )

def dostarczzamowienie(request):
	for element in request.POST.keys():
		if element[:3] == 'zam':
			zamowienie = Zamowienie.objects.get(id = int(element[3:]))
			zamowienie.dostarczono = True
			zamowienie.save()
	return HttpResponseRedirect("../obsluga/")

def obsluzzamowienie(request):
	for element in request.POST.keys():
		if element[:3] == 'zam':
			zamowienie = Zamowienie.objects.get(id = int(element[3:]))
			zamowienie.pracownik = request.user
			zamowienie.save()
	return HttpResponseRedirect("../obsluga/")


def zamowienie(request):
	menu = Pizza.objects.all()
	custom = PizzaKlienta.objects.filter(klient=request.user) if request.user.is_authenticated() else []
	dodatki = Dodatek.objects.all()
	adres = request.user.uzytkownik.adres if request.user.is_authenticated() else ''
	telefon = request.user.uzytkownik.telefon if request.user.is_authenticated() else ''
	return render(request, 'zamowienie.html', { 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })


def zlozzamowienie(request):
	menu = Pizza.objects.all()
	custom = PizzaKlienta.objects.filter(klient=request.user) if request.user.is_authenticated() else []
	dodatki = Dodatek.objects.all()
	adres = request.user.uzytkownik.adres if request.user.is_authenticated() else ''
	telefon = request.user.uzytkownik.telefon if request.user.is_authenticated() else ''

	# sprawdzamy, czy ilosci sa wartosciami liczbowymi i  czy nie
	# sumuja sie do zera

	laczna_ilosc = 0
	
	for pizza in menu:
		try:
			ilosc = int(request.POST['menu' + str(pizza.id)])
		except:
			return render(request, 'zamowienie.html', { 'error_message' : "Musisz podac wartosci liczbowe!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })
		else:
			if ilosc < 0:
				return render(request, 'zamowienie.html', { 'error_message' : "Podales ujenna ilosc!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })
			laczna_ilosc += ilosc

	for pizza in custom:
		try:
			ilosc = int(request.POST['custom' + str(pizza.id)])
		except:
			return render(request, 'zamowienie.html', { 'error_message' : "Musisz podac wartosci liczbowe!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })
		else:
			if ilosc < 0:
				return render(request, 'zamowienie.html', { 'error_message' : "Podales ujenna ilosc!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })
			laczna_ilosc += ilosc


	for dodatek in dodatki:
		try:
			ilosc = int(request.POST['dodatek' + str(dodatek.id)])
		except:
			return render(request, 'zamowienie.html', { 'error_message' : "Musisz podac wartosci liczbowe!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })
		else:
			if ilosc < 0:
				return render(request, 'zamowienie.html', { 'error_message' : "Podales ujenna ilosc!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })
			laczna_ilosc += ilosc
		
	if laczna_ilosc == 0:
		return render(request, 'zamowienie.html', { 'error_message' : "Musisz cos zamowic!", 'menu' : menu, 'custom' : custom, 'dodatki' : dodatki, 'adres' : adres, 'telefon' : telefon })
		
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
