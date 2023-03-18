# models/horario.py
from django.db import models

class Horario(models.Model):
    dia_semana = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    def __str__(self):
        return f'{self.dia_semana}: {self.hora_inicio} - {self.hora_fin}'
