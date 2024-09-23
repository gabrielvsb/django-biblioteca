from django.db import models
from django.db.models import F
from django.forms import ValidationError


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=60, blank=True, null=True, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "autores"

    def __str__(self):
        return self.nome
    

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    descricao = models.CharField(max_length=500)
    isbn = models.CharField(max_length=13)
    ativo = models.BooleanField(default=True)
    estoque = models.PositiveIntegerField(default=1)
    quantidade_total = models.PositiveIntegerField(default=1)
    livro_digital = models.FileField(upload_to='pdfs/', blank=True, null=True)
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.isbn} - {self.titulo}"
    
    def adicionar_estoque(self, quantidade=1):
        self.estoque += quantidade
        self.save()

    def remover_estoque(self, quantidade=1):
        if self.estoque >= quantidade:
            self.estoque -= quantidade
            self.save()
        else:
            raise ValueError("Não há estoque suficiente")

class Pessoa(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=60, blank=True, null=True, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField("Data do Empréstimo", auto_now_add=True)
    data_devolucao = models.DateTimeField("Data da Devolução", blank=True, null=True)

    class Meta:
        verbose_name_plural = "empréstimo"
        verbose_name_plural = "empréstimos"

    def __str__(self):
        return f"Emprestimo: {self.livro.titulo} para {self.pessoa.nome}"