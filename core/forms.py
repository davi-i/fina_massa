from django import forms
from django.db.models import F
from .models import (Ingrediente, ItemCardapio, Filial, Endereco, Pizza, Tipo, Promocao)
from django.utils.translation import ugettext_lazy as _


class DateTimeField(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        super().__init__(input_formats=['%Y-%m-%dT%H:%M'], *args, **kwargs)
        self.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})


class TimeField(forms.TimeField):
    def __init__(self, *args, **kwargs):
        super().__init__(input_formats=['%H:%M'], *args, **kwargs)
        self.widget = forms.TimeInput(attrs={'type': 'time'})


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ('nome',)

    def __init__(self, *args, **kwargs):
        super().__init__(use_required_attribute=False, *args, **kwargs)


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

    def __init__(self, *args, **kwargs):
        super().__init__(use_required_attribute=False, *args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        preco = cleaned_data.get('preco')
        tipo = cleaned_data.get('tipo')

        if tipo and tipo.descricao.startswith('pizza'):
            cleaned_data['preco'] = None
            return

        if not preco:
            self.add_error('preco', "Este campo é obrigatório")


class ItemCardapioEdicaoForm(ItemCardapioForm):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        self.fields['tipo'].widget.attrs = {'readonly': True}

    def clean(self):
        return super(forms.ModelForm, self).clean()


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ('rua',
                  'bairro',
                  'cidade',
                  'numero')


class FilialForm(forms.ModelForm):
    abertura = TimeField()
    fechamento = TimeField()

    class Meta:
        model = Filial
        fields = ('nome',
                  'contato',
                  'abertura',
                  'fechamento',)


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('preco',)

    def __init__(self, *args, **kwargs):
        super().__init__(use_required_attribute=False, *args, **kwargs)
        self.fields['preco'].label = ('Preço (%s)' %
                                      self.instance.tamanho.descricao)

    def save(self, item):
        pizza = super().save(commit=False)
        pizza.item = item
        pizza.save()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     preco = cleaned_data.get('preco')
    #     item = self.instance.item

    #     if not item.tipo.descricao.startswith('pizza'):
    #         raise forms.ValidationError('O ItemCardapio vinculado à pizza deve ser do tipo pizza')

    #     if not preco:
    #         self.add_error('preco', "Este campo é obrigatório")


class PizzaCricaoForm(PizzaForm):
    def __init__(self, tamanho, *args, **kwargs):
        super().__init__(instance=Pizza(tamanho=tamanho), *args, **kwargs)


class PromocaoForm(forms.ModelForm):
    inicio = DateTimeField()
    fim = DateTimeField()

    class Meta:
        model = Promocao
        fields = ('descricao', 'inicio', 'fim', 'itens')

        widgets = {
            'itens': forms.CheckboxSelectMultiple(),
        }