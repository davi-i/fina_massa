from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import (ItemCardapio)

class ItemCardapio(UserCreationForm):
    class Meta:
        model = ItemCardapio
        fiedls = ('descricao',
                  'tipo',
                  'preco',
                  'ingredientes',
                  'filiais')



        
        
    