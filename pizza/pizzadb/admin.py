from django.contrib import admin
from pizzadb import models
from pizzadb.models import Pizza, Dodatek, Skladnik

#admin.site.register( models.Klient )
admin.site.register(Pizza)
admin.site.register(Dodatek)
admin.site.register(Skladnik)
