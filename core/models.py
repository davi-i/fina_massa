from django.db import models

# Create your models here.


class Tipo(models.Model):
    descricao = models.CharField('Descrição', max_length=100)

    def __str__(self):
        return self.descricao.replace('_', ' ').capitalize()


class Ingrediente(models.Model):
    nome = models.CharField('Nome', max_length=100)

    def __str__(self):
        return self.nome.capitalize()

class Endereco(models.Model):
    rua = models.CharField('Rua', max_length=100)
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)

    def __str__(self):
        return '%s, %s, %s' % (self.rua, self.bairro, self.cidade)


class Filial(models.Model):
    nome = models.CharField('Nome', max_length=100)
    contato = models.IntegerField('Contato')
    endereco = models.ForeignKey(Endereco,
                                on_delete=models.PROTECT)

    def __str__(self):
        return self.nome.capitalize()


class ItemCardapio(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    tipo = models.ForeignKey(Tipo,
                             on_delete=models.CASCADE,
                             related_query_name='item')
    ingredientes = models.ManyToManyField(Ingrediente, blank=True)
    filiais = models.ManyToManyField(Filial, related_query_name='item')
    preco = models.DecimalField('Preço',
                                max_digits=10,
                                decimal_places=2,
                                null=True)

    class Meta:
        default_related_name = 'itens'

class Tamanho(models.Model):
    descricao = models.CharField('Tamanho', max_length=4)
    fatias = models.IntegerField('Fatias')


class Pizza(models.Model):
    item = models.ForeignKey(ItemCardapio,
                             on_delete=models.CASCADE,
                             limit_choices_to={
                                 'tipo__descricao___startswith': 'pizza'
                             })
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['item', 'tamanho']
        ordering = ['tamanho']
