﻿"""fina_massa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('senha/<int:id>/', views.senha, name='senha'),
    path('sobre/', views.sobre, name='sobre'),
    path(
        'cardapio/cadastrar/',
        views.cardapio_cadastro,
        name='cardapio_cadastro'
    ),
    path(
        'cardapio/<int:id>/editar/',
        views.cardapio_edicao,
        name='cardapio_edicao'
    ),
    path(
        'cardapio/<int:id>/remover/',
        views.cardapio_remocao,
        name='cardapio_remocao'
    ),
    path('cardapio/', views.cardapio, name='cardapio'),
    path('cardapio/itens', views.cardapio_itens, name='cardapio_itens'),
    path('filial/', views.filiais, name='filiais'),
    path('filial/cadastrar', views.filial_cadastro, name='filial_cadastro'),
    path('filial//<int:id>/editar', views.filial_edicao, name='filial_edicao'),
    path(
        'filial/<int:id>/remover', views.filial_remocao, name='filial_remocao'
    ),
    path('promocao/', views.promocoes, name='promocoes'),
    path(
        'promocao/cadastrar', views.promocao_cadastro, name='promocao_cadastro'
    ),
    path(
        'promocao/<int:id>/editar',
        views.promocao_edicao,
        name='promocao_edicao'
    ),
    path(
        'promocao/<int:id>/remover',
        views.promocao_remocao,
        name='promocao_remocao'
    ),
    path(
        'funcionario/cadastrar',
        views.funcionario_cadastro,
        name='funcionario_cadastro'
    ),
    path(
        'funcionario/<int:id>/editar',
        views.funcionario_edicao,
        name='funcionario_edicao'
    ),
    path(
        'funcionario/<int:id>/remover',
        views.funcionario_remocao,
        name='funcionario_remocao'
    ),
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('carrossel/cadastrar/', views.carrossel_cadastro, name='carrossel_cadastro'),
    path('carrossel/gerenciar/', views.carrossel_gerenciamento, name='carrossel_gerenciamento'),
    path('carrossel/<int:id>/remover/', views.carrossel_remocao, name='carrossel_remocao'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
