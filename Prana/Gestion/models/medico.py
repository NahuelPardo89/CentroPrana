from django.db import models
from .usuario import Usuario

from django.utils import timezone

class Medico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    especialidades = models.ManyToManyField('EspecialidadMedica')
    matricula = models.IntegerField()
    obra_social = models.ManyToManyField('ObraSocial', blank=True, through='PrecioConsulta', related_name='medicos')
    
    class Meta:
        verbose_name='Medico'
        verbose_name_plural = 'Medicos'

    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'

class EspecialidadMedica(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return self.nombre

class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class PrecioConsulta(models.Model):
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    obra_social = models.ForeignKey('ObraSocial', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vigencia = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.medico} - {self.obra_social}: {self.precio}'
    
    class Meta:
        unique_together = ('medico', 'obra_social')
    
class HorarioDia(models.Model):
    DIA_CHOICES = [
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miércoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sábado'),
        ('D', 'Domingo'),
    ]

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='horarios_dias')
    dia = models.CharField(max_length=1, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('medico', 'dia')
        verbose_name = 'Horario de Día'
        verbose_name_plural = 'Horarios de Días'
   
    def __str__(self):
        return f'{self.get_dia_display()} - {self.hora_inicio} - {self.hora_fin}'