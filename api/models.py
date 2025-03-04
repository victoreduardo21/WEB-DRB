from django.db import models


class Motorista(models.Model):
    placa = models.CharField(max_length=7)
    cpf = models.CharField(max_length=11)
