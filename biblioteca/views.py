from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from biblioteca.models import Livro, Emprestimo, Pessoa

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
    
    if request.method == 'POST':
        pessoa = Pessoa.objects.get(usuario=request.user)
        if not pessoa:
            messages.error(request, "Não é possível fazer emprestimo")
            return redirect('home')
        try:
            Emprestimo.objects.create(livro=livro, pessoa=pessoa)
        except ValidationError as error:
            messages.error(request, str(error))
            return redirect('home')

    context = {
        'livro': livro
    }
    return render(request, 'biblioteca/emprestimo.html', context)

def detalhes(request, pk):
    livro = Livro.objects.filter(pk=pk).first()
    if not livro:
        messages.error(request, "Livro não encontrado")
        return redirect('home')
    context = {
        'livro': livro
    }
    return render(request, 'biblioteca/detalhes.html', context)