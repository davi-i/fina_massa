from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'index': 'active'})


def sobre(request):
    return render(request, 'sobre.html', {'sobre': 'active'})


def cardapio_cadastro(request):
    return render(request, 'cardapio_cadastro.html')

def cardapio(request):
    return render(request, 'cardapio.html', {'cardapio': 'active'})

