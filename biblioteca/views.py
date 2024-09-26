from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from biblioteca.models import Livro

def home(request):
    livros = Livro.objects.all()
    context = {
        'livros': livros
    }
    return render(request, 'biblioteca/home.html', context)

@login_required(login_url='/account/login')
def emprestimo(request, pk):
    livro = Livro.objects.filter(pk=pk).first()
    if not livro:
        messages.error(request, "Livro não encontrado")
        return redirect('home')
    return render(request, 'biblioteca/emprestimo.html')

def detalhes(request, pk):
    livro = Livro.objects.filter(pk=pk).first()
    if not livro:
        messages.error(request, "Livro não encontrado")
        return redirect('home')

    context = {
        'livro': livro
    }
    return render(request, 'biblioteca/detalhes.html', context)