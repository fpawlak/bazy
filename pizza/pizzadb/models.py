from django.db import models
from django.contrib.auth.models import User

class Uzytkownik( models.Model ):

	imie = models.CharField( max_length = 20 )
	nazwisko = models.CharField( max_length = 50 )
	adres = models.CharField( max_length = 100 )
	telefon = models.CharField( max_length = 20 )
	funkcja = models.CharField( max_length = 1 )
	usrId = models.OneToOneField( User )

	def __unicode__( self ):
		return self.Imie + self.Nazwisko

#class Pracownik( models.Model ):
#
#	imie = models.CharField( max_length = 20 )
#	nazwisko = models.CharField( max_length = 50 )
#	adres = models.CharField( max_length = 100 )
#	telefon = models.CharField( max_length = 20 )
#	idUsr = models.OneToOneField( User )

class Skladnik( models.Model ):
	
	nazwa = models.CharField( max_length = 20 )
	cena = models.DecimalField( max_digits = 10, decimal_places = 2 )
	rodzaj = models.CharField( max_length = 1 )

	def __unicode__( self ):
		return self.nazwa


class PizzaKlienta( models.Model ):

	nazwa = models.CharField( max_length = 20 )
	klient = models.ForeignKey( User )
	cena = models.DecimalField( max_digits = 10, decimal_places = 2 )
	skladniki = models.ManyToManyField( Skladnik )

class Dodatek( models.Model ):

	nazwa = models.CharField( max_length = 20 )
	rodzaj = models.CharField( max_length = 1 )
	opis = models.CharField( max_length = 200 )
	cena = models.DecimalField( max_digits = 10, decimal_places = 2 )


class Pizza( models.Model ):
	
	nazwa = models.CharField( max_length = 20 )
	opis = models.CharField( max_length = 200 )
	cena = models.DecimalField( max_digits = 10, decimal_places = 2 )
	skladniki = models.ManyToManyField( Skladnik )

	def __unicode__( self ):
		return self.nazwa


class Zamowienie( models.Model ):
	
	klient = models.ForeignKey( User, related_name = 'skladajacy' )
	pracownik = models.ForeignKey( User, related_name = 'obslugujacy', blank = True, null = True )
	data = models.DateField()
	platnoscKarta = models.BooleanField()
	telefon = models.CharField( max_length = 20 )
	adres = models.CharField( max_length = 100 )
	kwota = models.DecimalField( max_digits = 10, decimal_places = 2 )
	dostarczono = models.BooleanField()
	pizze = models.ManyToManyField( Pizza, through = 'Zamowienie_Pizza' )
	pizzeKlienta = models.ManyToManyField( PizzaKlienta, through = 'Zamowienie_PizzaKlienta' )
	dodatek = models.ManyToManyField( Dodatek, through = 'Zamowienie_Dodatek' )

class Zamowienie_Dodatek( models.Model ):
	
	zamowienie = models.ForeignKey( Zamowienie )
	dodatek = models.ForeignKey( Dodatek )
	ilosc = models.IntegerField() 

class Zamowienie_Pizza( models.Model ):
	
	zamowienie = models.ForeignKey( Zamowienie )
	pizza = models.ForeignKey( Pizza )
	ilosc = models.IntegerField() 

class Zamowienie_PizzaKlienta( models.Model ):
	
	zamowienie = models.ForeignKey( Zamowienie )
	pizzaKlienta = models.ForeignKey( PizzaKlienta )
	ilosc = models.IntegerField() 

