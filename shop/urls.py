from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^index/$', views.index),
    url(r'^cart/$', views.cart),
    url(r'^login/$', views.login),
    url(r'^showProduct/$', views.showProduct),
    url(r'^checkout/$', views.checkout),
    url(r'^additem/$', views.add_to_cart, name='additem-url'),
    url(r'^removeitem/$', views.remove_from_cart, name='removeitem-url'),
]