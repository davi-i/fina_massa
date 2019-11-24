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


class TipoForm(forms.ModelForm):
    class Meta:
        model = models.ItemTipo
        fields = ('descricao', 'possui_ingredientes', 'possui_tamanhos')
        widgets = {
            'possui_ingredientes': forms.RadioSelect,
            'possui_tamanhos': forms.RadioSelect
        }


class TamanhoForm(forms.ModelForm):
    class Meta:
        model = models.Tamanho
        fields = ('descricao', 'fatias')


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
            'filiais': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(use_required_attribute=False, *args, **kwargs)
        self.fields['ingredientes'].required = False
        if not hasattr(self, 'tamanhos'):
            self.tamanhos = TamanhoFormSet(self.data or None)

    def clean(self):
        cleaned_data = super().clean()
        preco = cleaned_data.get('preco')
        tipo = cleaned_data.get('tipo')
        ingredientes = cleaned_data.get('ingredientes')

        self.possui_tamanhos = False
        if tipo:
            if tipo.possui_ingredientes and not ingredientes:
                self.add_error('ingredientes', 'Este campo é obrigatório')
            if tipo.possui_tamanhos:
                cleaned_data['preco'] = None
                self.possui_tamanhos = True
                return

        if not preco:
            self.add_error('preco', "Este campo é obrigatório")

    def is_valid(self):
        valido = super().is_valid()
        if self.possui_tamanhos:
            valido = valido and self.tamanhos.is_valid()
        return valido

    def save(self, commit=True):
        item = super().save(commit)
        if self.tamanhos:
            self.tamanhos.save(item, commit)


class ItemCardapioEdicaoForm(ItemCardapioForm):
    def __init__(self, item, data, *args, **kwargs):
        self.possui_tamanhos = item.tipo.possui_tamanhos
        if self.possui_tamanhos:
            self.tamanhos = TamanhoFormSet(
                data or None,
                queryset=item.tamanhos.all()
            )
        super().__init__(data, instance=item, *args, **kwargs)
        self.fields['tipo'].widget.attrs = {'readonly': True}

    def clean(self):
        super(forms.ModelForm, self).clean()
        if self.possui_tamanhos:
            self.tamanhos.clean()


class ItemTamanhoForm(forms.ModelForm):
    class Meta:
        model = models.ItemTamanho
        fields = ('preco',)

    def __init__(self, *args, **kwargs):
        if 'tamanho' in kwargs:
            kwargs['instance'] = models.ItemTamanho(tamanho=kwargs.pop('tamanho'))
        super().__init__(*args, **kwargs)
        self.tamanho = self.instance.tamanho
        self.fields['preco'].label = ('Preço (%s)' %
                                      self.tamanho.descricao)

    def save(self, commit=False):
        item_tamanho = super().save(commit=False)
        if hasattr(self, 'tamanho'):
            item_tamanho.tamanho = self.tamanho
        if commit:
            item_tamanho.save()
        return item_tamanho


class BaseTamanhoFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        if 'queryset' not in kwargs:
            self.tamanhos = models.Tamanho.objects.all()
            kwargs['queryset'] = models.ItemTamanho.objects.none()
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        if hasattr(self, 'tamanhos') and index < len(self.tamanhos):
            form_kwargs['tamanho'] = self.tamanhos[index]
        return form_kwargs

    def save(self, item, commit=True):
        itens_tamanho = super().save(commit=False)
        if commit:
            for item_tamanho in itens_tamanho:
                item_tamanho.item = item
                item_tamanho.save()
        return itens_tamanho


tamanho_count = models.Tamanho.objects.count()
TamanhoFormSet = forms.modelformset_factory(
    model=models.ItemTamanho,
    form=ItemTamanhoForm,
    formset=BaseTamanhoFormSet,
    max_num=tamanho_count,
    extra=tamanho_count
)


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
        model = models.Carrossel
        fields = ('imagem',)
