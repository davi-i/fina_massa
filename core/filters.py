import django_filters
from .models import ItemCardapio


class ItemCardapioFilter(django_filters.FilterSet):
    preco = django_filters.NumberFilter(label="Preço", lookup_expr='exact')
    preco_minimo = django_filters.NumberFilter(label="Preço mínimo",
                                               field_name='preco',
                                               lookup_expr='gt')
    preco_maximo = django_filters.NumberFilter(label="Preço máximo",
                                               field_name='preco',
                                               lookup_expr='lt')
    tipo = django_filters.CharFilter(label='Tipo', lookup_expr='icontains')

    class Meta:
        model = ItemCardapio
        fields = ['filiais']
