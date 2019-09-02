from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .filters import ItemCardapioFilter
from .models import ItemCardapio


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
    filter = ItemCardapioFilter(request.GET, queryset=itens)
    contexto = {
        'cardapio': 'active',
        'filter': filter,
    }
    return render(request, 'cardapio.html', contexto)
