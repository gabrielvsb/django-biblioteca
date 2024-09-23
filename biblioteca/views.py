from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from biblioteca.models import Livro

def home(request):
    livros = Livro.objects.all()
    context = {
        'livros': livros
    }
    return render(request, 'biblioteca/home.html', context)