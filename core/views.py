from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .filters import ItemCardapioFilter
from .models import ItemCardapio, Tamanho, Pizza, Tipo
from .forms import ItemCardapioForm, ItemCardapioEdicaoForm, FilialForm, EnderecoForm, PizzaForm, PizzaCricaoForm


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


@login_required
def cardapio_cadastro(request):
    pizzas_forms = []
    for n, tamanho in enumerate(Tamanho.objects.all(), start=1):
        pizzas_forms.append(PizzaCricaoForm(tamanho,
                                            request.POST or None,
                                            prefix=n,
                                            use_required_attribute=False))
    form = ItemCardapioForm(request.POST or None, use_required_attribute=False)
    if (form.is_valid() and
            all([pizza_form.is_valid() for pizza_form in pizzas_forms])):
        item = form.save()
        if form.cleaned_data['tipo'].descricao.startswith('pizza'):
            for pizza_form in pizzas_forms:
                pizza_form.save(item)
        return redirect('cardapio')
    contexto = {
        'form': form,
        'pizzas_forms': pizzas_forms,
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
            if form.cleaned_data['tipo'].descricao.startswith('pizza'):
                for pizza_form in pizzas_forms:
                    pizza_form.save(item)
            else:
                for pizza_form in pizzas_forms:
                    del pizza_form
        return redirect('cardapio')
    contexto = {
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
    }
    return render(request, 'cardapio.html', contexto)


def filial_cadastro(request):
    form = FilialForm(request.POST or None)
    endereco_form = EnderecoForm(request.POST or None)
    if form.is_valid() and endereco_form.is_valid():
        endereco = endereco_form.save()
        filial = form.save(commit=False)
        filial.endereco = endereco
        filial.save()
        return redirect('cardapio')
    contexto = {
        'form': form,
        'endereco_form': endereco_form
    }
    return render(request, 'filial_cadastro.html', contexto)
