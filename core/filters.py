import django_filters as filters
from django import forms
from .models import ItemCardapio, Filial, ItemTipo, ItemTamanho


class ItemCardapioFilter(filters.FilterSet):
    preco_minimo = filters.NumberFilter(label="Preço mínimo",
                                        field_name='preco',
                                        lookup_expr='gte')
    preco_maximo = filters.NumberFilter(label="Preço máximo",
                                        field_name='preco',
                                        lookup_expr='lte')
    tipo = filters.ModelMultipleChoiceFilter(
        queryset=ItemTipo.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    filiais = filters.ModelMultipleChoiceFilter(
        queryset=Filial.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ItemCardapio
        fields = []


class ItemTamanhoFilter(filters.FilterSet):
    preco_minimo = filters.NumberFilter(label="Preço mínimo",
                                        field_name='preco',
                                        lookup_expr='gte')
    preco_maximo = filters.NumberFilter(label="Preço máximo",
                                        field_name='preco',
                                        lookup_expr='lte')

    class Meta:
        model = ItemTamanho
        fields = []
