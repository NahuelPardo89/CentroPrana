from django.contrib import admin
from .models import (Usuario, Paciente, Medico, EspecialidadMedica, ObraSocial,
                     PrecioConsulta, Secretaria, Horario, Turno, Consulta)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'email', 'telefono', 'is_active', 'is_staff')
    search_fields = ('dni', 'nombre', 'apellido', 'email', 'telefono')
    list_filter = ('is_active', 'is_staff')

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'direccion', 'instagram', 'facebook', 'numero_obra_social')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'direccion')
    list_filter = ('obras_sociales',)

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'matricula')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'matricula')
    list_filter = ('especialidades', 'obra_social')

class SecretariaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'horario')
    search_fields = ('usuario__nombre', 'usuario__apellido')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(EspecialidadMedica)
admin.site.register(ObraSocial)
admin.site.register(PrecioConsulta)
admin.site.register(Secretaria, SecretariaAdmin)
admin.site.register(Horario)
admin.site.register(Turno)
admin.site.register(Consulta)
