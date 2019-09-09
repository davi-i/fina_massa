from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .filters import ItemCardapioFilter
from .models import ItemCardapio, Tamanho, Pizza, Tipo
from .forms import ItemCardapioForm


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
    form = ItemCardapioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cardapio')
    contexto = {
        'form': form,
    }
    return render(request, 'cardapio_cadastro.html', contexto)


def cardapio_edicao(request, id):
    item = ItemCardapio.objects.get(pk=id)
    form = ItemCardapioForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('cardapio')
    contexto = {
        'form': form,
    }
    return render(request, 'cardapio_cadastro.html', contexto)


def cardapio(request):
    item_filter = ItemCardapioFilter(request.GET,
                                     queryset=ItemCardapio.objects.all())
    itens = item_filter.qs
    tipos = Tipo.objects.filter(item__id__in=itens).distinct()
    tamanhos = Tamanho.objects.all()
    contexto = {
        'cardapio': 'active',
        'filter': item_filter,
        'tipos': tipos,
        'tamanhos': tamanhos,
    }
    return render(request, 'cardapio.html', contexto)
