# models/secretaria.py
from django.db import models
from .usuario import Usuario


class Secretaria(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    horario_entrada= models.CharField(max_length=5,blank=True)
    horario_salida= models.CharField(max_length=5,blank=True)
    class Meta:
        verbose_name = 'Secretaria'
        verbose_name_plural = 'Secretarias'

    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'
