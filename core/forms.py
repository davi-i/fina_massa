from django import forms
from django.db.models import F
from .models import (Ingrediente, ItemCardapio, Filial,
                     Endereco, Pizza, Tipo, Promocao, Tamanho)
from django.utils.translation import ugettext_lazy as _
import datetime


def fix_date(date):
    if type(date) is datetime.date:
        return date.strftime('%Y-%m-%d')
    elif type(date) is datetime.time:
        return date.strftime('%H:%M')
    return date.astimezone().strftime('%Y-%m-%dT%H:%M')


class DateTimeField(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        super().__init__(input_formats=['%Y-%m-%dT%H:%M'], *args, **kwargs)
        self.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})


class DateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        super().__init__(input_formats=['%Y-%m-%d'], *args, **kwargs)
        self.widget = forms.DateTimeInput(attrs={'type': 'date'})


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

    def __init__(self, data, *args, **kwargs):
        prefix = kwargs['prefix'] = 'endereco'
        if data:
                kwargs['data'] = {k: v for
                                  k, v in data.items()
                                  if k.startswith(prefix)} or None
        super().__init__(*args, **kwargs)


class FilialForm(forms.ModelForm):
    abertura = TimeField()
    fechamento = TimeField()

    class Meta:
        model = Filial
        fields = ('nome',
                  'foto',
                  'contato',
                  'abertura',
                  'fechamento',
                  'endereco')
        widgets = {
            'endereco': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        # kwargs['use_required_attribute'] = False
        kwargs['prefix'] = 'filial'
        super().__init__(*args, **kwargs)
        self.fields['endereco'].empty_label = None


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('preco',)

    def __init__(self, *args, **kwargs):
        if 'tamanho' in kwargs:
            tamanho = self.tamanho = kwargs.pop('tamanho')
            kwargs['instance'] = Pizza(tamanho=self.tamanho)
        else:
            tamanho = kwargs['instance'].tamanho
        super().__init__(*args, **kwargs)
        self.fields['preco'].label = ('Preço (%s)' %
                                      tamanho.descricao)

    def save(self, commit=False):
        pizza = super().save(commit=False)
        if hasattr(self, 'tamanho'):
            pizza.tamanho = self.tamanho
        if commit:
            pizza.save()
        return pizza
    # def clean(self):
    #     cleaned_data = super().clean()
    #     preco = cleaned_data.get('preco')
    #     item = self.instance.item

    #     if not item.tipo.descricao.startswith('pizza'):
    #         raise forms.ValidationError('O ItemCardapio vinculado à pizza deve ser do tipo pizza')

    #     if not preco:
    #         self.add_error('preco', "Este campo é obrigatório")


class BasePizzaFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        if 'queryset' not in kwargs:
            self.tamanhos = Tamanho.objects.all()
            kwargs['queryset'] = Pizza.objects.none()
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        if hasattr(self, 'tamanhos') and index < len(self.tamanhos):
            form_kwargs['tamanho'] = self.tamanhos[index]
        return form_kwargs

    def save(self, item):
        pizzas = super().save(commit=False)
        for pizza in pizzas:
            pizza.item = item
            pizza.save()
        return pizzas


tamanho_count = Tamanho.objects.count()
PizzaFormSet = forms.modelformset_factory(model=Pizza,
                                          form=PizzaForm,
                                          formset=BasePizzaFormSet,
                                          max_num=tamanho_count,
                                          extra=tamanho_count)


class PromocaoForm(forms.ModelForm):
    data = DateField()

    class Meta:
        model = Promocao
        fields = ('imagem', 'filial', 'data', 'itens')

        widgets = {
            'itens': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs and kwargs['instance'].pk:
            kwargs['instance'].data = fix_date(kwargs['instance'].data)
        super().__init__(*args, **kwargs)
