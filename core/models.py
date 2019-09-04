from django.db import models

# Create your models here.


class ItemCardapio(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    tipo = models.CharField('Tipo', max_length=100)
    preco = models.DecimalField(
        'Preço', max_digits=10, decimal_places=2, null=True)
    ingredientes = models.CharField('Ingredientes', max_length=100)
    filiais = models.CharField('Filiais', max_length=100)


class Tamanho(models.Model):
    descricao = models.CharField('Tamanho', max_length=4)
    fatias = models.IntegerField('Fatias')


class TamanhoPizza(models.Model):
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    pizza = models.ForeignKey(ItemCardapio,
                              limit_choices_to=(
                                  models.Q(tipo='pizza') |
                                  models.Q(tipo='pizza_especial')
                              ),
                              on_delete=models.CASCADE)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
