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
        fields = ('especialidades', 'matricula')
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
        fields = ['horario_entrada','horario_salida']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['direccion', 'instagram', 'facebook', 'numero_obra_social', 'obras_sociales']
        widgets = {
            'obras_sociales': CheckboxSelectMultiple(),
        }



class TurnoForm(forms.ModelForm):
    HORAS_DISPONIBLES = [
        (f'{hora}:{minutos:02d}', f'{hora}:{minutos:02d}') for hora in range(8, 21) for minutos in (0, 30)
    ]

    hora_numero = forms.ChoiceField(choices=HORAS_DISPONIBLES, label="Hora")

    class Meta:
        model = Turno
        fields = ['paciente', 'medico', 'fecha', 'obra_social', 'confirmado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

    def __init__(self, *args, paciente_id=None, medico_id=None, **kwargs):
        self.paciente_id = paciente_id
        self.medico_id = medico_id
        super().__init__(*args, **kwargs)

        if self.paciente_id and self.medico_id:
            paciente = Paciente.objects.get(pk=self.paciente_id)
            medico = Medico.objects.get(pk=self.medico_id)

            self.fields['paciente'] = forms.ModelChoiceField(
                queryset=Paciente.objects.filter(pk=self.paciente_id),
                initial=self.paciente_id,
                widget=forms.Select(attrs={'readonly': True, 'style': 'pointer-events: none;'})
            )
            self.fields['medico'] = forms.ModelChoiceField(
                queryset=Medico.objects.filter(pk=self.medico_id),
                initial=self.medico_id,
                widget=forms.Select(attrs={'readonly': True, 'style': 'pointer-events: none;'})
            )

            obras_sociales = ObraSocial.objects.filter(paciente=paciente, medicos=medico)

            if obras_sociales:
                self.fields['obra_social'].queryset = obras_sociales
            else:
                particular = ObraSocial.objects.get(nombre="PARTICULAR")
                self.fields['obra_social'].queryset = ObraSocial.objects.filter(pk=particular.pk)

            self.fields['obra_social'].required = True
            self.fields['obra_social'].empty_label = None

        if self.instance and self.instance.hora:
            self.initial['hora_numero'] = self.instance.hora.strftime('%H:%M')
            self.initial['fecha'] = self.instance.fecha

    def clean_hora_numero(self):
        hora_numero = self.cleaned_data['hora_numero']
        hour, minute = map(int, hora_numero.split(':'))
        return time(hour=hour, minute=minute)

    def save(self, commit=True):
        turno = super().save(commit=False)
        turno.hora = self.cleaned_data['hora_numero']
        if commit:
            turno.save()
        return turno

class SeleccionMedicoPacienteForm(forms.Form):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), label="Paciente")
    medico = forms.ModelChoiceField(queryset=Medico.objects.all(), label="Médico")


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['turno', 'precio']