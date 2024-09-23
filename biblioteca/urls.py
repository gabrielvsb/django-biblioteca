from django.contrib import admin
from django.urls import path
import biblioteca.views as views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
]
