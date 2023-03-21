from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory,CheckboxSelectMultiple
from .models import Medico, Usuario,PrecioConsulta,ObraSocial, Secretaria,Paciente,Turno, Consulta
from datetime import time
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellido', 'email',  'telefono','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', ValidationError('Las contraseñas no coinciden'))

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni','nombre', 'apellido', 'email',  'telefono']

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ('especialidades', 'matricula','horario')
        widgets = {
            'especialidades': CheckboxSelectMultiple(),
        }

class PrecioConsultaCreateForm(forms.ModelForm):
    class Meta:
        model = PrecioConsulta
        fields = ['obra_social', 'precio', 'fecha_vigencia']

    def __init__(self, *args, **kwargs):
        self.medico = kwargs.pop('medico')
        super(PrecioConsultaCreateForm, self).__init__(*args, **kwargs)
        self.fields['obra_social'].queryset = ObraSocial.objects.exclude(precioconsulta__medico=self.medico)

class PrecioConsultaUpdateForm(forms.ModelForm):
    class Meta:
        model = PrecioConsulta
        fields = ['obra_social', 'precio', 'fecha_vigencia']



class SecretariaForm(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ['horario']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['direccion', 'instagram', 'facebook', 'numero_obra_social', 'obras_sociales']
        widgets = {
            'obras_sociales': CheckboxSelectMultiple(),
        }

class TurnoForm(forms.ModelForm):
    hora_numero = forms.IntegerField(min_value=8, max_value=20, label="Hora")

    class Meta:
        model = Turno
        fields = ['paciente', 'medico', 'fecha', 'obra_social', 'confirmado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.hora:
            self.initial['hora_numero'] = self.instance.hora.hour
            self.initial['fecha'] = self.instance.fecha

    def clean_hora_numero(self):
        hora_numero = self.cleaned_data['hora_numero']
        return time(hour=hora_numero)

    def save(self, commit=True):
        turno = super().save(commit=False)
        turno.hora = self.cleaned_data['hora_numero']
        if commit:
            turno.save()
        return turno

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['turno', 'precio']