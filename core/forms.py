from django import forms

from .models import (ItemCardapio, Filial)


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

class FilialForm(forms.ModelForm):
  class Meta:
    model = Filial
    fields = ('nome',)
