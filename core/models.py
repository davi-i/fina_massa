from django.db import models

# Create your models here.

class ItemCardapio(Models.model):
	Tipo = models.Charfield('Tipo', max_length=100)
	Preco = models.Charfield('Preco', FIELDNAME = forms.FloatField())
	Ingredientes = models.Charfield('Ingredientes', max_length=100)
	FiliaisD = models.Charfield('FiliaisD', max_length=100)

		