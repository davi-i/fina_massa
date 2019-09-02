import django_filters
from .models import ItemCardapio


class ItemCardapioFilter(django_filters.Filter):
    class Meta:
        model = ItemCardapio
        fields = ['tipo', 'preco', 'filial']
