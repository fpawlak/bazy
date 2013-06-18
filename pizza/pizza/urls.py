from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pizza.views.home', name='home'),
    # url(r'^pizza/', include('pizza.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls) ),
	url(r'^menu/$', 'pizzadb.views.menu' ),
	url(r'^wlasnapizza/$', 'pizzadb.views.wlasnapizza' ),
    url(r'^dodajpizze/$', 'pizzadb.views.dodajpizze'),
                       url(r'^mojepizze/$', 'pizzadb.views.mojepizze'),                       
	url(r'^logowanie/$', 'pizzadb.views.logowanie' ),
	url(r'^log/$', 'pizzadb.views.log' ),
        url(r'^obsluga/$', 'pizzadb.views.obsluga' ),
        url(r'^zamowienie/$', 'pizzadb.views.zamowienie' ),
                       url(r'^zlozzamowienie/$', 'pizzadb.views.zlozzamowienie'),
url(r'^wyloguj/$', 'pizzadb.views.wyloguj' ),
url(r'^rejestracja/$', 'pizzadb.views.rejestracja' ),
url(r'^rejestruj/$', 'pizzadb.views.rejestruj' )
)
