from django.db import models

# Create your models here.


class ItemCardapio(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    tipo = models.CharField('Tipo', max_length=100)
    preco = models.FloatField('Preco')
    ingredientes = models.CharField('Ingredientes', max_length=100)
    filiais = models.CharField('Filiais', max_length=100)
