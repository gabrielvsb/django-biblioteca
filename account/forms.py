from django import forms
from biblioteca.models import Pessoa

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ["nome", "cpf", "email"]