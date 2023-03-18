# models/turno.py
from django.db import models
from django.utils import timezone
from .paciente import Paciente
from .medico import Medico, ObraSocial
from django.db.models.signals import post_save
from django.dispatch import receiver

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    obra_social = models.ForeignKey(ObraSocial, on_delete=models.SET_NULL, null=True, blank=True)
    confirmado = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f'Turno con {self.paciente} el {self.fecha} a las {self.hora}'

@receiver(post_save, sender=Turno)
def crear_consulta(sender, instance, created, **kwargs):
    if instance.confirmado:
        obra_social = instance.obra_social
        if obra_social:
            precio = instance.medico.obra_social.through.objects.get(
                medico=instance.medico,
                obra_social=obra_social
            ).precio
        else:
            precio = instance.medico.obra_social.through.objects.filter(
                medico=instance.medico
            ).first().precio
        Consulta.objects.create(turno=instance, precio=precio)

class Consulta(models.Model):
    turno = models.OneToOneField(Turno, on_delete=models.CASCADE, related_name='consulta')
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Consulta de {self.turno.paciente} con {self.turno.medico} el {self.turno.fecha} a las {self.turno.hora}'
