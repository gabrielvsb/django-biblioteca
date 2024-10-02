from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from biblioteca.models import Livro, Emprestimo, Pessoa

def home(request):
    livros = Livro.objects.all()
    livros_com_emprestimo = []

    if request.user:
        try:
            pessoa = Pessoa.objects.get(usuario=request.user)
        except Pessoa.DoesNotExist:
            pessoa = None

        livros_com_emprestimo = []

        if pessoa:
            emprestimos_ativos = Emprestimo.objects.filter(pessoa=pessoa, data_devolucao__isnull=True)
            livros_com_emprestimo = [emprestimo.livro.id for emprestimo in emprestimos_ativos]

    context = {
        'livros': livros,
        'livros_com_emprestimo': livros_com_emprestimo
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

@login_required(login_url='/account/login')
def devolucao(request, pk):
    livro = Livro.objects.filter(pk=pk).first()
    if not livro:
        messages.error(request, "Livro não encontrado")
        return redirect('home')
    
    pessoa = Pessoa.objects.get(usuario=request.user)
    if not pessoa:
        messages.error(request, "Não é possível devolver o livro")
        return redirect('home')
    try:
        emprestimo = Emprestimo.objects.get(livro=livro, pessoa=pessoa, data_devolucao__isnull=True)
    except ValidationError as error:
        messages.error(request, str(error))
        return redirect('home')

    if request.method == 'POST':
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()
        messages.success(request, f'Livro "{livro.titulo}" devolvido com sucesso!')
        return redirect('home')

    context = {
        'livro': livro
    }
    return render(request, 'biblioteca/devolucao.html', context)

def detalhes(request, pk):
    livro = Livro.objects.filter(pk=pk).first()
    if not livro:
        messages.error(request, "Livro não encontrado")
        return redirect('home')
    context = {
        'livro': livro
    }
    return render(request, 'biblioteca/detalhes.html', context)