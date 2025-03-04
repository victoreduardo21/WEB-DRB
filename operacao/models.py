from django.db import models


class Terminal(models.Model):
    nome = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    raio = models.IntegerField()

    def __str__(self):
        return self.nome


class Caminhoneiro(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    id_motorista = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
