from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'index.html', {'index': 'active'})

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
    return render(request, 'sobre.html', {'sobre': 'active'})

def cardapio_cadastro(request):
    return render(request, 'cardapio_cadastro.html')

def cardapio(request):
    return render(request, 'cardapio.html', {'cardapio': 'active'})

