from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField("CPF", max_length=11, unique=True)


class ItemTipo(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    possui_ingredientes = models.BooleanField(
        'Esse tipo possui ingredientes?',
        choices=((True, 'Sim'), (False, 'Não')),
        default=False
    )
    possui_tamanhos = models.BooleanField(
        'Esse tipo possui tamanhos?',
        choices=((True, 'Sim'), (False, 'Não')),
        default=False
    )

    def __str__(self):
        return self.descricao.replace('_', ' ').capitalize()


class Ingrediente(models.Model):
    nome = models.CharField('Nome', max_length=100, unique=True)

    def __str__(self):
        return self.nome.capitalize()


class Endereco(models.Model):
    rua = models.CharField('Rua', max_length=100)
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    numero = models.IntegerField('Número', null=True, blank=True)

    def __str__(self):
        numero = self.numero or "S/N"

        return '%s, %s, %s, %s' % (self.rua, self.bairro, self.cidade, numero)


class Filial(models.Model):
    nome = models.CharField('Nome', max_length=100, unique=True)
    foto = models.ImageField('Foto', upload_to='filiais')
    contato = models.IntegerField('Contato')
    endereco = models.ForeignKey(Endereco,
                                 on_delete=models.PROTECT,
                                 verbose_name='Endereço')
    abertura = models.TimeField()
    fechamento = models.TimeField()

    def __str__(self):
        return self.nome.capitalize()

    @property
    def contato_str(self):
        contato = str(self.contato)
        hifen = 7 if len(contato) == 11 else 6
        return '(' + contato[:2] + ') ' + contato[2:hifen] + '-' + contato[hifen:]


class ItemCardapio(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    tipo = models.ForeignKey(ItemTipo,
                             on_delete=models.CASCADE,
                             related_query_name='item')
    ingredientes = models.ManyToManyField(
        Ingrediente,
        related_query_name='item'
    )
    filiais = models.ManyToManyField(Filial, related_query_name='item')
    preco = models.DecimalField(
        'Preço',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        default_related_name = 'itens'
        ordering = ['tipo']

    def __str__(self):
        return "%s de %s" % (self.tipo, self.descricao.lower())

    @property
    def promocao_atual(self):
        try:
            return self.promocoes.get(data=timezone.now().date())
        except Promocao.DoesNotExist:
            return Promocao.objects.none()


class Tamanho(models.Model):
    descricao = models.CharField('Tamanho', max_length=4)
    fatias = models.IntegerField('Fatias')


class ItemTamanho(models.Model):
    item = models.ForeignKey(ItemCardapio,
                             on_delete=models.CASCADE,
                             limit_choices_to={
                                 'tipo__possui_tamanhos': True
                             },
                             related_name='tamanhos')
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('item', 'tamanho')
        ordering = ['tamanho']


class Promocao(models.Model):
    imagem = models.ImageField('Imagem', upload_to="promocoes")
    data = models.DateField('Data', unique=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    itens = models.ManyToManyField(ItemCardapio,
                                   verbose_name='Itens afetados',
                                   related_name='promocoes',
                                   related_query_name='promocao')

    def na_semana():
        promocoes = []
        agora = timezone.now()
        hoje = agora.date()

        def proper_week_day(weekday):
            if weekday == 6:
                return 0
            return weekday + 1
        # Começa do domingo dessa semana
        for i in range(7):
            dia = hoje - timedelta(days=proper_week_day(hoje.weekday()) - i)
        # Hoje fica no meio
        # for i in range(-3, 4):
        #     dia = hoje - timedelta(days=i)
        # Começa de hoje
        # for i in range(7):
        #     dia = hoje + timedelta(days=i)
            try:
                promocao = Promocao.objects.get(data=dia)
            except Promocao.DoesNotExist:
                promocao = None
            is_hoje = 'hoje' if timezone.localtime(agora).date() == dia else ''
            promocoes.append(((dia, is_hoje), promocao))
        return promocoes


class Carrossel(models.Model):
    imagem = models.ImageField('Imagem', upload_to="carrossel")

    def __str__(self):
        return self.imagem.path
