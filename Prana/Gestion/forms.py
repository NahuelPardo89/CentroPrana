from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory,CheckboxSelectMultiple
from .models import Medico, Usuario,PrecioConsulta,ObraSocial, Secretaria,Paciente

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
        fields = ['horario']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['direccion', 'instagram', 'facebook', 'numero_obra_social', 'obras_sociales']