from django.contrib import admin
from django.urls import path
import account.views as views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
]
