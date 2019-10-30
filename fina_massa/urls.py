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
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(extra_context={'restrito': 'active'}), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),
    # path('perfil/', perfil, name='perfil'),
    path('sobre/', views.sobre, name='sobre'),
    path('cardapio/cadastrar/', views.cardapio_cadastro, name='cardapio_cadastro'),
    path('cardapio/<int:id>/editar/', views.cardapio_edicao, name='cardapio_edicao'),
    path('cardapio/<int:id>/remover/', views.cardapio_remocao, name='cardapio_remocao'),
    path('cardapio/', views.cardapio, name='cardapio'),
    path('filial/cadastrar', views.filial_cadastro, name='filial_cadastro'),
    path('promocao/', views.promocoes, name='promocoes'),
    path('promocao/cadastrar', views.promocao_cadastro, name='promocao_cadastro'),
    path('promocao/<int:id>/editar', views.promocao_edicao, name='promocao_edicao'),
    path('promocao/<int:id>/remover', views.promocao_remocao, name='promocao_remocao'),
    path('funcionarios/', views.funcionarios, name='funcionarios'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
