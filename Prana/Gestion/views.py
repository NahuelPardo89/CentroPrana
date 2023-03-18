from django.urls import reverse_lazy
from django.shortcuts import render,HttpResponseRedirect, redirect,get_object_or_404
from django.contrib.auth.models import Group

from django.views import generic
from .models import Paciente, Medico, Secretaria
from django.urls import reverse_lazy
from django.views import generic

#models
from .models import Usuario, Medico, Secretaria, ObraSocial, PrecioConsulta, EspecialidadMedica

#forms
from .forms import UsuarioForm,UsuarioUpdateForm, MedicoForm,PrecioConsultaCreateForm,PrecioConsultaUpdateForm,UsuarioUpdateForm, SecretariaForm



# Vistas de Usuario
class UsuarioListView(generic.ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'

class UsuarioCreateView(generic.CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

class UsuarioUpdateView(generic.UpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm
    template_name = 'usuario/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

class UsuarioDeleteView(generic.DeleteView):
    model = Usuario
    template_name = 'usuario/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

# Vistas de Medico
class MedicoListView(generic.ListView):
    model = Medico
    template_name = 'medico/medico_list.html'

class MedicoCreateView(generic.CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medico/medico_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['usuario_form'] = UsuarioForm(self.request.POST)
        else:
            context['usuario_form'] = UsuarioForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        usuario_form = context['usuario_form']
        if usuario_form.is_valid():
            
            usuario = usuario_form.save(commit=False)
            usuario.is_staff = True
            usuario.set_password(usuario.password)
            usuario.save()
            medicos_group, created = Group.objects.get_or_create(name="Medicos")
            usuario.groups.add(medicos_group)
            medico = form.save(commit=False)
            medico.usuario = usuario
            medico.save()
            form.save_m2m()
            return redirect('medico_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class MedicoUpdateView(generic.UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medico/medico_form.html'
    success_url = reverse_lazy('medico_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['usuario_form'] = UsuarioUpdateForm(self.request.POST, instance=self.object.usuario)
        else:
            context['usuario_form'] = UsuarioUpdateForm(instance=self.object.usuario)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        usuario_form = context['usuario_form']
        if usuario_form.is_valid():
            usuario_form.save()
            medico = form.save(commit=False)
            medico.usuario = self.object.usuario
            medico.save()
            form.save_m2m()
            return redirect('medico_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class MedicoDeleteView(generic.DeleteView):
    model = Medico
    template_name = 'medico/medico_confirm_delete.html'
    success_url = reverse_lazy('medico_list')

    def post(self, request, *args, **kwargs):
        medico = self.get_object()
        usuario = medico.usuario
        response = super().post(request, *args, **kwargs)
        usuario.delete()
        return response
#vistas para cargar el precio de la consulta para cada obra social
class MedicoObraSocialListView(generic.ListView):
    model = PrecioConsulta
    template_name = 'medico/medico_precioconsulta_list.html'
    context_object_name = 'precioconsulta_list'

    def get_queryset(self):
        self.medico = Medico.objects.get(pk=self.kwargs['pk'])
        return PrecioConsulta.objects.filter(medico=self.medico)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medico'] = self.medico
        return context

class PrecioConsultaCreateView(generic.CreateView):
    model = PrecioConsulta
    form_class = PrecioConsultaCreateForm
    template_name = 'medico/precioconsulta_form.html'

    def get_success_url(self):
        return reverse_lazy('medico_precioconsulta_list', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        medico = Medico.objects.get(pk=self.kwargs['pk'])
        form.instance.medico = medico
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        medico = Medico.objects.get(pk=self.kwargs['pk'])
        kwargs['medico'] = medico
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medico'] = Medico.objects.get(pk=self.kwargs['pk'])
        return context


class PrecioConsultaUpdateView(generic.UpdateView):
    model = PrecioConsulta
    form_class = PrecioConsultaUpdateForm
    template_name = 'medico/precioconsulta_form.html'

    def get_success_url(self):
        return reverse_lazy('medico_precioconsulta_list', kwargs={'pk': self.object.medico.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        medico_pk = self.kwargs['medico_pk']  # Cambiar 'pk' a 'medico_pk'
        return queryset.filter(medico__pk=medico_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medico'] = Medico.objects.get(pk=self.kwargs['medico_pk'])
        return context

class PrecioConsultaDeleteView(generic.DeleteView):
    model = PrecioConsulta
    template_name = 'medico/precioconsulta_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('medico_precioconsulta_list', kwargs={'pk': self.object.medico.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        medico_pk = self.kwargs['medico_pk']
        return queryset.filter(medico__pk=medico_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medico'] = Medico.objects.get(pk=self.kwargs['medico_pk'])  # Cambiar 'pk' a 'medico_pk'
        return context

# Vistas de Secretaria
class SecretariaListView(generic.ListView):
    model = Secretaria
    template_name = 'secretaria/secretaria_list.html'

class SecretariaCreateView(generic.CreateView):
    model = Secretaria
    form_class = SecretariaForm
    template_name = 'secretaria/secretaria_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['usuario_form'] = UsuarioForm(self.request.POST)
        else:
            context['usuario_form'] = UsuarioForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        usuario_form = context['usuario_form']
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            usuario.is_staff = True
            usuario.set_password(usuario.password)
            usuario.save()
            secretarias_group, created = Group.objects.get_or_create(name="Secretarias")
            usuario.groups.add(secretarias_group)
            secretaria = form.save(commit=False)
            secretaria.usuario = usuario
            secretaria.save()
            return redirect('secretaria_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))

class SecretariaUpdateView(generic.UpdateView):
    model = Secretaria
    form_class = SecretariaForm
    template_name = 'secretaria/secretaria_form.html'
    success_url = reverse_lazy('secretaria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['usuario_form'] = UsuarioForm(self.request.POST, instance=self.object.usuario)
        else:
            context['usuario_form'] = UsuarioForm(instance=self.object.usuario)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        usuario_form = context['usuario_form']
        if usuario_form.is_valid():
            usuario_form.save()
            secretaria = form.save(commit=False)
            secretaria.usuario = self.object.usuario
            secretaria.save()
            return redirect('secretaria_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))

class SecretariaDeleteView(generic.DeleteView):
    model = Secretaria
    template_name = 'secretaria/secretaria_confirm_delete.html'
    success_url = reverse_lazy('secretaria_list')

    def post(self, request, *args, **kwargs):
        secretaria = self.get_object()
        usuario = secretaria.usuario
        response = super().post(request, *args, **kwargs)
        usuario.delete()
        return response

class PacienteListView(generic.ListView):
    model = Paciente
    template_name = 'paciente/paciente_list.html'
# ... Vistas de Paciente ...
class PacienteCreateView(generic.CreateView):
    model = Paciente
    fields = '__all__'
    template_name = 'paciente/paciente_form.html'
    success_url = reverse_lazy('paciente_list')

class PacienteUpdateView(generic.UpdateView):
    model = Paciente
    fields = '__all__'
    template_name = 'paciente/paciente_form.html'
    success_url = reverse_lazy('paciente_list')

class PacienteDeleteView(generic.DeleteView):
    model = Paciente
    template_name = 'paciente/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

#vistas obra social

from django.urls import reverse_lazy
from django.views import generic
from .models import ObraSocial

class ObraSocialListView(generic.ListView):
    model = ObraSocial
    template_name = 'obraSocial/obra_social_list.html'

class ObraSocialCreateView(generic.CreateView):
    model = ObraSocial
    fields = '__all__'
    template_name = 'obraSocial/obra_social_form.html'
    success_url = reverse_lazy('obra_social_list')

class ObraSocialUpdateView(generic.UpdateView):
    model = ObraSocial
    fields = '__all__'
    template_name = 'obraSocial/obra_social_form.html'
    success_url = reverse_lazy('obra_social_list')

class ObraSocialDeleteView(generic.DeleteView):
    model = ObraSocial
    template_name = 'obraSocial/obra_social_confirm_delete.html'
    success_url = reverse_lazy('obra_social_list')


#vistas especialidad medica


class EspecialidadMedicaListView(generic.ListView):
    model = EspecialidadMedica
    template_name = 'especialidadMedica/especialidad_medica_list.html'

class EspecialidadMedicaCreateView(generic.CreateView):
    model = EspecialidadMedica
    fields = '__all__'
    template_name = 'especialidadMedica/especialidad_medica_form.html'
    success_url = reverse_lazy('especialidad_medica_list')

class EspecialidadMedicaUpdateView(generic.UpdateView):
    model = EspecialidadMedica
    fields = '__all__'
    template_name = 'especialidadMedica/especialidad_medica_form.html'
    success_url = reverse_lazy('especialidad_medica_list')

class EspecialidadMedicaDeleteView(generic.DeleteView):
    model = EspecialidadMedica
    template_name = 'especialidadMedica/especialidad_medica_confirm_delete.html'
    success_url = reverse_lazy('especialidad_medica_list')