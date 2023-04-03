from django.db import models
from .usuario import Usuario
from datetime import datetime, timedelta

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
    # obtiene turnos disponibles para una fecha pasada como argumento
    def turnos_disponibles(self, fecha):
        dia_semana = fecha.strftime('%A')
        dia_semana_espanol = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
        }
        dia_semana = dia_semana_espanol.get(dia_semana, dia_semana)

        horarios_dias = self.horarios_dias.filter(dia=dia_semana).order_by('hora_inicio')
        if not horarios_dias:
            return []

        turnos = []
        citas_programadas = self.turnos.filter(fecha=fecha)  # Utiliza la relación inversa aquí

        for horario_dia in horarios_dias:
            hora_actual = horario_dia.hora_inicio
            while hora_actual < horario_dia.hora_fin:
                cita_programada = citas_programadas.filter(hora=hora_actual).exists()
                if not cita_programada:
                    turnos.append(hora_actual)
                
                # Convierte los objetos time a datetime, realiza la suma y luego extrae la hora
                hora_actual_dt = datetime.combine(fecha, hora_actual)
                hora_actual_dt += timedelta(minutes=30)
                hora_actual = hora_actual_dt.time()

        return turnos

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
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sabado', 'Sábado'),
        
    ]

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='horarios_dias')
    dia = models.CharField(max_length=9, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('medico', 'dia')
        verbose_name = 'Horario de Día'
        verbose_name_plural = 'Horarios de Días'
   
    def __str__(self):
        return f'{self.get_dia_display()} - {self.hora_inicio} - {self.hora_fin}'