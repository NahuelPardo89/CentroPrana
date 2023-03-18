# models/secretaria.py
from django.db import models
from .usuario import Usuario
from .horario import Horario

class Secretaria(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    horario = models.OneToOneField(Horario, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Secretaria'
        verbose_name_plural = 'Secretarias'

    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'
