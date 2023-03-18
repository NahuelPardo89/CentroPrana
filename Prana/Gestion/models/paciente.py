# models/paciente.py
from django.db import models
from .usuario import Usuario

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    direccion = models.CharField(max_length=70)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    numero_obra_social = models.CharField(max_length=50, null=True, blank=True)
    obras_sociales = models.ManyToManyField('ObraSocial', blank=True)

    class Meta:
        verbose_name='Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'
