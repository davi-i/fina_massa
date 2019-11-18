from django.test import TestCase


'''
Código para criar tamanhos, tipos, filiais e alguns itens
'''
from core.models import *
from django.contrib.auth.models import User

p = Tamanho.objects.create(descricao="P", fatias=4)
m = Tamanho.objects.create(descricao="M", fatias=6)
g = Tamanho.objects.create(descricao="G", fatias=8)

pastel = ItemTipo.objects.create(descricao='pastel')
pizza = ItemTipo.objects.create(descricao='pizza')
pizza_especial = ItemTipo.objects.create(descricao='pizza_especial')
suco = ItemTipo.objects.create(descricao='suco')
bebida = ItemTipo.objects.create(descricao='bebida')

mussarela = Ingrediente.objects.create(nome='mussarela')
frango = Ingrediente.objects.create(nome='frango')
catupiry = Ingrediente.objects.create(nome='catupiry')
calabresa = Ingrediente.objects.create(nome='calabresa')

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
        i.descricao = d
        i.save()
        for ig in igs:
            i.ingredientes.add(ig)
        if tipo.descricao.startswith('pizza'):
            for (t, pt) in zip(Tamanho.objects.all(), p):
                Pizza.objects.create(item=i, tamanho=t, preco=pt)
        else:
            i.preco = p
        i.save()



u = User.objects.create(
    first_name="Bruna",
    last_name="Francelino",
    username="bruna",
    is_staff=True
)
u.set_password('finamassa.123')
u.save()
Usuario.objects.create(
    cpf="00000000000",
    user=u
)

Carrossel.objects.create()