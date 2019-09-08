from django.test import TestCase
from .models import *

# Create your tests here.
p = Tamanho.objects.create(descricao="P", fatias=4)
m = Tamanho.objects.create(descricao="M", fatias=6)
g = Tamanho.objects.create(descricao="G", fatias=8)

pastel = Tipo.objects.create(descricao='pastel')
pizza = Tipo.objects.create(descricao='pizza')
pizza_especial = Tipo.objects.create(descricao='pizza_especial')
suco = Tipo.objects.create(descricao='suco')
bebida = Tipo.objects.create(descricao='bebida')

mussarela = Ingrediente.objects.create(nome='mussarela')
frango = Ingrediente.objects.create(nome='frango')
catupiry = Ingrediente.objects.create(nome='catupiry')
calabresa = Ingrediente.objects.create(nome='calabresa')

bf = Filial.objects.create(nome='BF')
cang = Filial.objects.create(nome='Cang')

tipos = [pastel, pizza, suco]
descricoes = [
    ['Queijo', 'Frango', 'Frango com Catupiry'],
    ['Mussarela', 'Frango', 'Calabresa'],
    ['Uva', 'Goiaba']
]
precos = [
    [8.0, 9.0, 10.0],
    [[20.0, 25.0, 30.0], [25.0, 30.0, 35.0], [23.0, 28.0, 33.0]],
    [5.0, 5.0],
]
ingredientes = [
    [[mussarela], [frango], [frango, catupiry]],
    [[mussarela], [mussarela, frango], [mussarela, calabresa]],
    [[] * 3],
]
for tipo, ds, ps, igss in zip(tipos, descricoes, precos, ingredientes):
    for d, p, igs in zip(ds, ps, igss):
        i = ItemCardapio()
        i.tipo = tipo
        i.save()
        i.filiais.add(bf)
        i.filiais.add(cang)
        for ig in igs:
            i.ingredientes.add(ig)
        if tipo.descricao.startswith('pizza'):
            for (t, pt) in zip(Tamanho.objects.all(), p):
                Pizza.objects.create(item=i, tamanho=t, preco=pt)
        else:
            i.preco = p
        i.save()
