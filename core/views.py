from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .filters import ItemCardapioFilter
from .models import ItemCardapio, Tamanho


def index(request):
    contexto = {
        'index': 'active',
    }
    return render(request, 'index.html', contexto)


def registro(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    contexto = {
        'form': form,
    }
    return render(request, 'registration/registro.html', contexto)


def perfil(request):
    return render(request, 'registration/perfil.html')


def sobre(request):
    contexto = {
        'sobre': 'active',
    }
    return render(request, 'sobre.html', contexto)


def cardapio_cadastro(request):
    return render(request, 'cardapio_cadastro.html')


def cardapio(request):
    itens = ItemCardapio.objects.all()
    item_filter = ItemCardapioFilter(request.GET, queryset=itens)
    itens = item_filter.qs
    pasteis = itens.filter(tipo='pastel')
    pizzas = itens.filter(tipo='pizza')
    pizzas_especiais = itens.filter(tipo='pizza_especial')
    sucos = itens.filter(tipo='suco')
    bebidas = itens.filter(tipo='bebida')
    tamanhos = Tamanho.objects.all()
    contexto = {
        'cardapio': 'active',
        'filter': item_filter,
        'pasteis': pasteis,
        'pizzas': pizzas,
        'pizzas_especiais': pizzas_especiais,
        'sucos': sucos,
        'bebidas': bebidas,
        'tamanhos': tamanhos,
    }
    return render(request, 'cardapio.html', contexto)
