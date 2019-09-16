from django import forms

from .models import (ItemCardapio, Filial, Endereco, Pizza)


class ItemCardapioForm(forms.ModelForm):
    class Meta:
        model = ItemCardapio
        fields = ('descricao',
                  'tipo',
                  'preco',
                  'ingredientes',
                  'filiais')
        widgets = {
            'ingredientes': forms.CheckboxSelectMultiple(),
            'filiais': forms.CheckboxSelectMultiple(),
        }


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ('rua',
                  'bairro',
                  'cidade')


class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = ('nome',
                  'contato',)


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('preco',)
