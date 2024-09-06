from typing import Any
from django.contrib import admin
from django.db.models import F
from django.utils.safestring import mark_safe
from biblioteca.models import Autor, Livro, Pessoa, Emprestimo, Categoria

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome',)
    list_per_page = 50

admin.site.register(Autor, AutorAdmin)

class LivroAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'titulo', 'ativo', 'estoque', 'arquivo_link')
    search_fields = ('isbn', 'titulo')
    list_per_page = 50

    def arquivo_link(self, obj):
        if obj.livro_digital:
            return mark_safe(f'<a href="{obj.livro_digital.url}" target="_blank">Acessar o livro</a>')
        return "Nenhum arquivo"
    
    arquivo_link.short_description = 'Arquivo'

    def save_model(self, request, obj, form, change):
        if obj.quantidade_total != obj.estoque:
            obj.estoque = obj.quantidade_total
        return super().save_model(request, obj, form, change)

admin.site.register(Livro, LivroAdmin)

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'cpf')
    list_per_page = 50

admin.site.register(Pessoa, PessoaAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    search_fields = ('nome',)
    list_per_page = 50

admin.site.register(Categoria, CategoriaAdmin)

class EmprestimoAdmin(admin.ModelAdmin):
    model = Emprestimo
    list_display = ('get_nome_pessoa', 'get_titulo_livro', 'data_emprestimo', 'data_devolucao')
    list_per_page = 50

    def get_titulo_livro(self, obj):
        return obj.livro.titulo
    get_titulo_livro.admin_order_field  = 'livro'
    get_titulo_livro.short_description = 'Titulo do livro'

    def get_nome_pessoa(self, obj):
        return obj.pessoa.nome
    get_nome_pessoa.admin_order_field  = 'pessoa'
    get_nome_pessoa.short_description = 'Nome'

    def save_model(self, request, obj, form, change):
        if obj.livro.pk:
            obj.livro.remover_estoque()
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.livro.pk:
            obj.livro.adicionar_estoque()
        
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.livro.pk:
                obj.livro.adicionar_estoque()

        return super().delete_queryset(request, queryset)
    

admin.site.register(Emprestimo, EmprestimoAdmin)
