from django import forms
from django.contrib.auth.models import User
from . import models
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


class UsuarioForm(forms.ModelForm):
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'username')

    class Meta:
        model = models.Usuario
        fields = ('cpf',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        has_instance = bool(self.instance.pk)
        user = self.instance.user if has_instance else None
        self.user_form = UsuarioForm.UserForm(self.data, instance=user)
        self.fields['permissao'] = forms.ChoiceField(
            choices=[
                (0, 'Apenas um funcionário'),
                (1, 'Um propietário')
            ],
            label="O funcionário é"
        )
        if has_instance:
            self.initial['permissao'] = int(self.instance.user.is_staff)
        self.fields.update(self.user_form.fields)
        self.initial.update(self.user_form.initial)
        self.fields['first_name'].label = "Nome"
        self.fields['last_name'].label = "Sobrenome"

    def is_valid(self):
        return super().is_valid() and self.user_form.is_valid()

    def save(self, commit=True):
        usuario = super().save(commit=False)
        user = self.user_form.save(commit=False)
        if self.cleaned_data['permissao'] == '1':
            user.is_staff = True
        user.set_password('finamassa.' + usuario.cpf)
        if commit:
            user.save()
            usuario.user = user
            usuario.save()
        return usuario


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = models.Ingrediente
        fields = ('nome',)

    def __init__(self, *args, **kwargs):
        super().__init__(use_required_attribute=False, *args, **kwargs)


class ItemCardapioForm(forms.ModelForm):
    class Meta:
        model = models.ItemCardapio
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
        if not hasattr(self, 'pizzas'):
            self.pizzas = PizzaFormSet(self.data or None)

    def clean(self):
        cleaned_data = super().clean()
        preco = cleaned_data.get('preco')
        tipo = cleaned_data.get('tipo')

        if tipo and tipo.descricao.startswith('pizza'):
            cleaned_data['preco'] = None
            self.is_pizza = True
            return
        self.is_pizza = False

        if not preco:
            self.add_error('preco', "Este campo é obrigatório")

    def is_valid(self):
        valido = super().is_valid()
        if self.is_pizza:
            valido = valido and self.pizzas.is_valid()
        return valido

    def save(self, commit=True):
        item = super().save(commit)
        if self.is_pizza:
            self.pizzas.save(item, commit)


class ItemCardapioEdicaoForm(ItemCardapioForm):
    def __init__(self, item, data, *args, **kwargs):
        self.is_pizza = item.tipo.descricao.startswith('pizza')
        if self.is_pizza:
            self.pizzas = PizzaFormSet(
                data or None,
                queryset=item.pizza_set.all()
            )
        super().__init__(data, instance=item, *args, **kwargs)
        self.fields['tipo'].widget.attrs = {'readonly': True}

    def clean(self):
        super(forms.ModelForm, self).clean()
        if self.is_pizza:
            self.pizzas.clean()


class PizzaForm(forms.ModelForm):
    class Meta:
        model = models.Pizza
        fields = ('preco',)

    def __init__(self, *args, **kwargs):
        if 'tamanho' in kwargs:
            kwargs['instance'] = models.Pizza(tamanho=kwargs.pop('tamanho'))
        super().__init__(*args, **kwargs)
        self.tamanho = self.instance.tamanho
        self.fields['preco'].label = ('Preço (%s)' %
                                      self.tamanho.descricao)

    def save(self, commit=False):
        pizza = super().save(commit=False)
        if hasattr(self, 'tamanho'):
            pizza.tamanho = self.tamanho
        if commit:
            pizza.save()
        return pizza


class BasePizzaFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        if 'queryset' not in kwargs:
            self.tamanhos = models.Tamanho.objects.all()
            kwargs['queryset'] = models.Pizza.objects.none()
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        if hasattr(self, 'tamanhos') and index < len(self.tamanhos):
            form_kwargs['tamanho'] = self.tamanhos[index]
        return form_kwargs

    def save(self, item, commit=True):
        pizzas = super().save(commit=False)
        if commit:
            for pizza in pizzas:
                pizza.item = item
                pizza.save()
        return pizzas


tamanho_count = models.Tamanho.objects.count()
PizzaFormSet = forms.modelformset_factory(model=models.Pizza,
                                          form=PizzaForm,
                                          formset=BasePizzaFormSet,
                                          max_num=tamanho_count,
                                          extra=tamanho_count)


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = models.Endereco
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
        model = models.Filial
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
        kwargs['prefix'] = 'filial'
        if 'instance' in kwargs and kwargs['instance'].pk:
            kwargs['instance'].abertura = fix_date(kwargs['instance'].abertura)
            kwargs['instance'].fechamento = fix_date(kwargs['instance'].fechamento)
        super().__init__(*args, **kwargs)
        self.fields['endereco'].empty_label = None


class PromocaoForm(forms.ModelForm):
    data = DateField()

    class Meta:
        model = models.Promocao
        fields = ('imagem', 'filial', 'data', 'itens')

        widgets = {
            'itens': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs and kwargs['instance'].pk:
            kwargs['instance'].data = fix_date(kwargs['instance'].data)
        super().__init__(*args, **kwargs)


class CarrosselForm(forms.ModelForm):

    class Meta:
        model = models.CarrosselImagem
        fields = ('arquivo',)


    def save(self, commit=True):
        imagem = super().save(commit=False)
        imagem.carrossel = models.Carrossel.objects.get(id=1)
        if commit:
            imagem.save()
        return imagem
        
