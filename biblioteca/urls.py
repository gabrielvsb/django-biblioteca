from django.contrib import admin
from django.urls import path
import biblioteca.views as views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('emprestimo/<int:pk>', views.emprestimo, name='emprestimo'),
    path('devolucao/<int:pk>', views.devolucao, name='devolucao'),
    path('detalhes/<int:pk>', views.detalhes, name='detalhes'),
]
