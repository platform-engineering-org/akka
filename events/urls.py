from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.event, name='event'),
    path('thanks/', views.thanks, name='thanks'),
    path('events/', views.events, name='events'),
]
