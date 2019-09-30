"""fina_massa URL Configuration

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
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("registro/", registro, name="registro"),
    path('perfil/', perfil, name='perfil'),
    path('sobre/', sobre, name='sobre'),
    path('cardapio/cadastrar/', cardapio_cadastro, name='cardapio_cadastro'),
    path('cardapio/<int:id>/editar/', cardapio_edicao, name='cardapio_edicao'),
    path('cardapio/<int:id>/remover/', cardapio_remocao, name='cardapio_remocao'),
    path('cardapio/', cardapio, name='cardapio'),
    path('filial/cadastrar', filial_cadastro, name='filial_cadastro'),
    path('promocao/cadastrar', promocao_cadastro, name='promocao_cadastro')
]
