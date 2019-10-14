from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .filters import ItemCardapioFilter
from .models import Ingrediente, ItemCardapio, Tamanho, Tipo, Filial, Promocao
from .forms import (IngredienteForm, ItemCardapioForm, ItemCardapioEdicaoForm, FilialForm,
                    EnderecoForm, PizzaForm, PizzaCricaoForm, PromocaoForm)
from datetime import datetime


def promocao_atual():
    try:
        return Promocao.objects.filter(inicio__lte=datetime.now(),
                                       fim__gte=datetime.now()).earliest('fim')
    except Promocao.DoesNotExist:
        return Promocao.objects.none()


def index(request):
    filiais = Filial.objects.all()
    contexto = {
        'index': 'active',
        'filiais': filiais,
        'promocao': promocao_atual(),
    }
    return render(request, 'index.html', contexto)


@login_required
def registro(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    contexto = {
        'restrito': 'active',
        'registro': 'active',
        'form': form,
    }
    return render(request, 'registration/registro.html', contexto)


def sobre(request):
    contexto = {
        'sobre': 'active',
        'promocao': promocao_atual(),
    }
    return render(request, 'sobre.html', contexto)


@login_required
def cardapio_cadastro(request):
    form = ItemCardapioForm(request.POST or None)
    pizzas_forms = []
    for n, tamanho in enumerate(Tamanho.objects.all(), start=1):
        pizzas_forms.append(PizzaCricaoForm(tamanho,
                                            request.POST or None,
                                            prefix=n))
    ingrediente_form = IngredienteForm(request.POST or None)
    if ('salvar-ingrediente' in request.POST and
            ingrediente_form.is_valid()):
        ingrediente_form.save()
        ingrediente_form = IngredienteForm()
    elif ('salvar-item' in request.POST and
          form.is_valid() and
          all([pizza_form.is_valid() for pizza_form in pizzas_forms])):
        item = form.save()
        if form.cleaned_data['tipo'].descricao.startswith('pizza'):
            for pizza_form in pizzas_forms:
                pizza_form.save(item)
        return redirect('cardapio')
    contexto = {
        'restrito': 'active',
        'cardapio_cadastro': 'active',
        'form': form,
        'pizzas_forms': pizzas_forms,
        'ingrediente_form': ingrediente_form
    }
    return render(request, 'cardapio_cadastro.html', contexto)


@login_required
def cardapio_edicao(request, id):
    item = get_object_or_404(ItemCardapio, pk=id)
    pizzas_forms = []
    for n, pizza in enumerate(item.pizza_set.all(), start=1):
        pizzas_forms.append(PizzaForm(request.POST or None,
                                      prefix=n,
                                      instance=pizza,
                                      use_required_attribute=False))
    form = ItemCardapioEdicaoForm(item, request.POST or None)
    if form.is_valid():
        item = form.save()
        if all([pizza_form.is_valid() for pizza_form in pizzas_forms]):
            for pizza_form in pizzas_forms:
                pizza_form.save(item)
        return redirect('cardapio')
    contexto = {
        'restrito': 'active',
        'cardapio_cadastro': 'active',
        'form': form,
        'pizzas_forms': pizzas_forms,
    }
    return render(request, 'cardapio_cadastro.html', contexto)


@login_required
def cardapio_remocao(request, id):
    item = get_object_or_404(ItemCardapio, pk=id)
    item.delete()
    return redirect('cardapio')


def cardapio(request):
    item_filter = ItemCardapioFilter(request.GET,
                                     queryset=ItemCardapio.objects.all())
    tipos = []
    for tipo in Tipo.objects.all():
        tipos += [tipo.itens.filter(id__in=item_filter.qs)]
    tamanhos = Tamanho.objects.all()
    contexto = {
        'cardapio': 'active',
        'filter': item_filter,
        'tipos': tipos,
        'tamanhos': tamanhos,
        'promocao': promocao_atual(),
    }
    return render(request, 'cardapio.html', contexto)


@login_required
def filial_cadastro(request):
    form = FilialForm(request.POST or None, request.FILES or None)
    endereco_form = EnderecoForm(request.POST or None)
    if form.is_valid() and endereco_form.is_valid():
        endereco = endereco_form.save()
        filial = form.save(commit=False)
        filial.endereco = endereco
        filial.save()
        return redirect('cardapio')
    contexto = {
        'restrito': 'active',
        'filial_cadastro': 'active',
        'form': form,
        'endereco_form': endereco_form
    }
    return render(request, 'filial_cadastro.html', contexto)


@login_required
def promocao_cadastro(request):
    form = PromocaoForm(request.POST or None)
    if form.is_valid():
        form.save_m2m()
        form.save()
        return redirect('index')
    contexto = {
        'restrito': 'active',
        'promocao_cadastro': 'active',
        'form': form,
    }
    return render(request, 'promocao_cadastro.html', contexto)
