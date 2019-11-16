from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from . import filters, models, forms
from datetime import date


def redirect_to_next(request, other_page=None):
    return redirect(request.GET.get('next') or other_page)


def login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        if user.last_login is not None:
            auth_login(request, user)
            return redirect_to_next(request, settings.LOGIN_REDIRECT_URL)
        else:
            return senha(request, user.id)
    contexto = {
        'restrito': 'active',
        'form': form,
    }
    return render(request, 'registration/login.html', contexto)


def senha(request, id):
    if request.method == 'POST':
        if request.path == '/login/':
            data = None
        elif request.path == '/senha/%d/' % id:
            data = request.POST
        else:
            return redirect('login')

        user = User.objects.get(pk=id)
        form = SetPasswordForm(user, data=data)
        if form.is_valid():
            form.save()
            auth_login(request, user)
            return redirect_to_next(request, settings.LOGIN_REDIRECT_URL)
        contexto = {
            'restrito': 'active',
            'form': form,
            'name': user.first_name,
            'id': user.id,
        }
        return render(request, 'registration/senha.html', contexto)
    return redirect('login')


def index(request):
    filiais = models.Filial.objects.all()
    imagens = models.CarrosselImagem.objects.all()
    contexto = {
        'index': 'active',
        'filiais': filiais,
        'promocoes': models.Promocao.na_semana(),
        'imagens': imagens,
    }
    return render(request, 'index.html', contexto)


def sobre(request):
    contexto = {
        'sobre': 'active',
    }
    return render(request, 'sobre.html', contexto)


@login_required
def cardapio_itens(request):
    cardapio_itens = models.ItemCardapio.objects.all()
    contexto = {
        'restrito': 'active',
        'cardapio_gerenciar': 'active',
        'itens': cardapio_itens,
    }
    return render(request, 'cardapio_itens.html', contexto)


@login_required
def cardapio_cadastro(request):
    form = forms.ItemCardapioForm(request.POST or None)
    ingrediente_form = forms.IngredienteForm(request.POST or None)

    if ('salvar-ingrediente' in request.POST and
            ingrediente_form.is_valid()):
        ingrediente_form.save()
        ingrediente_form = forms.IngredienteForm()

    elif ('salvar-item' in request.POST and
          form.is_valid()):
        form.save()
        return redirect('cardapio')

    contexto = {
        'restrito': 'active',
        'cardapio_gerenciar': 'active',
        'titulo': 'Cadastrar item no cardápio',
        'form': form,
        'ingrediente_form': ingrediente_form
    }
    return render(request, 'cardapio_cadastro.html', contexto)


@login_required
def cardapio_edicao(request, id):
    item = get_object_or_404(models.ItemCardapio, pk=id)
    form = forms.ItemCardapioEdicaoForm(item, request.POST or None)
    ingrediente_form = forms.IngredienteForm(request.POST or None)

    if ('salvar-ingrediente' in request.POST and
            ingrediente_form.is_valid()):
        ingrediente_form.save()
        ingrediente_form = forms.IngredienteForm()
    elif ('salvar-item' in request.POST and
          form.is_valid()):
        form.save()
        return redirect('cardapio')
    contexto = {
        'restrito': 'active',
        'cardapio_gerenciar': 'active',
        'titulo': 'Editar item do cardápio',
        'form': form,
        'ingrediente_form': ingrediente_form
    }
    return render(request, 'cardapio_cadastro.html', contexto)


@login_required
def cardapio_remocao(request, id):
    item = get_object_or_404(models.ItemCardapio, pk=id)
    item.delete()
    return redirect('cardapio_itens')


def cardapio(request):
    item_filter = filters.ItemCardapioFilter(
        request.GET,
        queryset=models.ItemCardapio.objects.all()
    )
    pizza_filter = filters.PizzaFilter(
        request.GET,
        queryset=models.Pizza.objects.all()
    )
    tipos = []
    for tipo in models.Tipo.objects.all():
        itens = tipo.itens.filter(id__in=item_filter.qs)
        if tipo.descricao.startswith('pizza'):
            itens = itens.filter(pizza__in=pizza_filter.qs).distinct()
        tipos.append(itens)
    tamanhos = models.Tamanho.objects.all()
    contexto = {
        'cardapio': 'active',
        'filter': item_filter,
        'tipos': tipos,
        'tamanhos': tamanhos,
    }
    return render(request, 'cardapio.html', contexto)


@login_required
def filiais(request):
    filiais = models.Filial.objects.all()
    contexto = {
        'restrito': 'active',
        'filial_gerenciar': 'active',
        'filiais': filiais,
    }
    return render(request, 'filiais.html', contexto)


@login_required
def filial_cadastro(request):
    data = request.POST.copy() or None
    form = forms.FilialForm(data, request.FILES or None)
    endereco_form = forms.EnderecoForm(data)
    if endereco_form.is_valid():
        endereco = endereco_form.save()
        data['filial-endereco'] = endereco.pk
    if form.is_valid():
        form.save()
        return redirect('index')
    contexto = {
        'restrito': 'active',
        'filial_cadastro': 'active',
        'titulo': 'Cadastrar filial',
        'form': form,
        'endereco_form': endereco_form
    }
    return render(request, 'filial_cadastro.html', contexto)


@login_required
def filial_edicao(request, id):
    filial = get_object_or_404(models.Filial, pk=id)
    data = request.POST.copy() or None
    form = forms.FilialForm(data, request.FILES or None, instance=filial)
    endereco_form = forms.EnderecoForm(data)
    if endereco_form.is_valid():
        endereco = endereco_form.save()
        data['filial-endereco'] = endereco.pk
    if form.is_valid():
        form.save()
        return redirect('filiais')
    contexto = {
        'restrito': 'active',
        'filial_gerenciar': 'active',
        'titulo': 'Editar filial',
        'form': form,
        'endereco_form': endereco_form
    }
    return render(request, 'filial_cadastro.html', contexto)


@login_required
def filial_remocao(request):
    filial = get_object_or_404(models.Filial, pk=id)
    filial.delete()
    return redirect('filiais')


@login_required
def promocoes(request):
    promocoes = models.Promocao.objects.all()
    contexto = {
        'restrito': 'active',
        'promocao_gerenciar': 'active',
        'promocoes': promocoes,
    }
    return render(request, 'promocoes.html', contexto)


@login_required
def promocao_cadastro(request):
    form = forms.PromocaoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('promocoes')
    contexto = {
        'restrito': 'active',
        'promocao_gerenciar': 'active',
        'titulo': 'Cadastrar promoção',
        'form': form,
    }
    return render(request, 'promocao_cadastro.html', contexto)


@login_required
def promocao_edicao(request, id):
    promocao = get_object_or_404(models.Promocao, pk=id)
    form = forms.PromocaoForm(request.POST or None, instance=promocao)
    if form.is_valid():
        form.save()
        return redirect('index')
    contexto = {
        'restrito': 'active',
        'promocao_gerenciar': 'active',
        'titulo': 'Editar promoção',
        'form': form,
    }
    return render(request, 'promocao_cadastro.html', contexto)


@login_required
def promocao_remocao(request, id):
    promocao = get_object_or_404(models.Promocao, pk=id)
    promocao.delete()
    return redirect('promocoes')


@login_required
@staff_member_required(login_url='/login/')
def funcionarios(request):
    funcionarios = User.objects.all()
    contexto = {
        'restrito': 'active',
        'funcionario_gerenciar': 'active',
        'funcionarios': funcionarios,
    }
    return render(request, 'funcionarios.html', contexto)


@login_required
@staff_member_required(login_url='/login/')
def funcionario_cadastro(request):
    form = forms.UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('funcionarios')
    contexto = {
        'restrito': 'active',
        'funcionario_gerenciar': 'active',
        'titulo': 'Cadastrar funcionário',
        'form': form,
    }
    return render(request, 'registration/registro.html', contexto)


@login_required
@staff_member_required(login_url='/login/')
def funcionario_edicao(request, id):
    funcionario = get_object_or_404(User, pk=id).usuario
    form = forms.UsuarioForm(request.POST or None, instance=funcionario)
    if form.is_valid():
        form.save()
        return redirect('funcionarios')
    contexto = {
        'restrito': 'active',
        'funcionario_gerenciar': 'active',
        'titulo': 'Editar funcionário',
        'form': form,
    }
    return render(request, 'registration/registro.html', contexto)


@login_required
@staff_member_required(login_url='/login/')
def funcionario_remocao(request, id):
    funcionario = get_object_or_404(User, pk=id)
    funcionario.delete()
    return redirect('funcionarios')

@login_required
def carrossel_cadastro(request):
    form = forms.CarrosselForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('carrossel_gerenciamento')
    contexto = {
        'restrito': 'active',
        'carrossel_gerenciamento': 'active',
        'titulo': 'Cadastrar imagem',
        'form': form,
    }
    return render(request, 'carrossel_cadastro.html', contexto)


def carrossel_gerenciamento(request):
    imagens = models.CarrosselImagem.objects.all()
    contexto = {
        'restrito': 'active',
        'carrossel_gerenciar': 'active',
        'imagens': imagens,
    }
    return render(request, 'carrossel_gerenciamento.html', contexto)


def carrossel_remocao(request, id):
    imagem = models.CarrosselImagem.get(pk=id)
    imagem.delete()
    return redirect('carrossel_gerenciamento')

