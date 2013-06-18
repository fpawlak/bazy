from django.conf.urls import patterns, url

from pizzadb import views

urlpatterns = patterns('',

	url( r'^$', views.index )

)
