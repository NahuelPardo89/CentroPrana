from django.urls import reverse_lazy, reverse
from django.shortcuts import render,HttpResponseRedirect, redirect,get_object_or_404
from django.contrib.auth.models import Group

from django.views import generic



from .models import Paciente, Medico, Secretaria
from django.urls import reverse_lazy
from django.views import generic

#models
from .models import Usuario, Medico, Secretaria, ObraSocial, PrecioConsulta, EspecialidadMedica,Turno,Consulta, HorarioDia

#forms
from .forms import (UsuarioForm,UsuarioUpdateForm, MedicoForm,PrecioConsultaCreateForm,PrecioConsultaUpdateForm,
UsuarioUpdateForm, SecretariaForm,PacienteForm, TurnoForm, ConsultaForm,SeleccionMedicoPacienteForm, HorarioDiaForm)



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
            self.object = form.save(commit=False)  
            self.object.usuario = usuario
            self.object.save()
            form.save_m2m()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    def get_success_url(self):
        return reverse_lazy('medico_precioconsulta_create', kwargs={'pk': self.object.usuario.id})

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

class HorarioDiaListView(generic.ListView):
    template_name = 'medico/horario_list.html'
    context_object_name = 'horarios'

    def get_queryset(self):
        medico_id = self.kwargs['medico_id']
        return HorarioDia.objects.filter(medico_id=medico_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medico_id'] = self.kwargs['medico_id']
        return context

class HorarioDiaCreateView(generic.CreateView):
    model = HorarioDia
    form_class = HorarioDiaForm
    template_name = 'medico/horario_form.html'

    def form_valid(self, form):
        medico_id = self.kwargs['medico_id']
        medico = Medico.objects.get(pk=medico_id)
        dia = form.cleaned_data['dia']

        if HorarioDia.objects.filter(medico=medico, dia=dia).exists():
            form.add_error('dia', 'Ya existe un horario para este médico y este día')
            return self.form_invalid(form)

        form.instance.medico = medico
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            form.add_error(None, 'Error de integridad en la base de datos')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('horario_list', kwargs={'medico_id': self.kwargs['medico_id']})

class HorarioDiaUpdateView(generic.UpdateView):
    model = HorarioDia
    form_class = HorarioDiaForm
    template_name = 'medico/horario_form.html'
    context_object_name = 'horario'

    def get_success_url(self):
        medico_id = self.object.medico.pk
        return reverse_lazy('horario_list', kwargs={'medico_id': medico_id})

class HorarioDiaDeleteView(generic.DeleteView):
    model = HorarioDia
    template_name = 'medico/horario_confirm_delete.html'
    context_object_name = 'horario'

    def get_success_url(self):
        return reverse_lazy('horario_list', kwargs={'medico_id': self.object.medico.pk})



# Vistas de Secretaria
class SecretariaListView(generic.ListView):
    model = Secretaria
    template_name = 'secretaria/secretaria_list.html'

class SecretariaCreateView(generic.CreateView):
    model = Secretaria
    fields = SecretariaForm
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
            context['usuario_form'] = UsuarioUpdateForm(self.request.POST, instance=self.object.usuario)
        else:
            context['usuario_form'] = UsuarioUpdateForm(instance=self.object.usuario)
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


# ... Vistas de Paciente ...

class PacienteListView(generic.ListView):
    model = Paciente
    template_name = 'paciente/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 10

    def get_queryset(self):
        return Paciente.objects.order_by('usuario__apellido')

class PacienteCreateView(generic.CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'

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
            usuario.set_password(usuario.password)
            usuario.save()
            pacientes_group, created = Group.objects.get_or_create(name="Pacientes")
            usuario.groups.add(pacientes_group)
            paciente = form.save(commit=False)
            paciente.usuario = usuario
            paciente.save()
            form.save_m2m()
            return redirect('paciente_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PacienteUpdateView(generic.UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente/paciente_form.html'
    success_url = reverse_lazy('paciente_list')

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
            paciente = form.save(commit=False)
            paciente.usuario = self.object.usuario
            paciente.save()
            form.save_m2m()
            return redirect('paciente_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PacienteDeleteView(generic.DeleteView):
    model = Paciente
    template_name = 'paciente/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

    def post(self, request, *args, **kwargs):
        paciente = self.get_object()
        usuario = paciente.usuario
        response = super().post(request, *args, **kwargs)
        usuario.delete()
        return response

#vistas obra social



class HomeView(generic.TemplateView):
    def get_template_names(self):
        if not self.request.user.is_authenticated:
            return ['home.html']
        
        if self.request.user.groups.filter(name="Medicos").exists():
            return ['medico/home.html']
        elif self.request.user.groups.filter(name="Secretarias").exists():
            return ['secretaria/home.html']
        else:
            return ['paciente/home.html']

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

class TurnoListView(generic.ListView):
    model = Turno
    template_name = 'turno/turno_list.html'
    success_url = reverse_lazy('turno_list')

class SeleccionMedicoPacienteView(generic.FormView):
    form_class = SeleccionMedicoPacienteForm
    template_name = 'turno/seleccion_medico_paciente.html'

    def form_valid(self, form):
        paciente_id = form.cleaned_data['paciente'].pk
        medico_id = form.cleaned_data['medico'].pk
        return HttpResponseRedirect(reverse('turno_create', args=(paciente_id, medico_id)))
class TurnoCreateView(generic.CreateView):
    model = Turno
    form_class = TurnoForm 
    template_name = 'turno/turno_form.html'
    success_url = reverse_lazy('turno_list')

    def get_form(self, form_class=None):
        paciente_id = self.kwargs['paciente_id']
        medico_id = self.kwargs['medico_id']

        if form_class is None:
            form_class = self.get_form_class()

        form = form_class(paciente_id=paciente_id, medico_id=medico_id, **self.get_form_kwargs())

        return form

"""
class TurnoCreateView(generic.CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turno/turno_form.html'
    success_url = reverse_lazy('turno_list')
"""    
class TurnoUpdateView(generic.UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turno/turno_form.html'
    success_url = reverse_lazy('turno_list')
class TurnoDeleteView(generic.DeleteView):
    model = Turno
    template_name = 'turno/turno_confirm_delete.html'
    success_url = reverse_lazy('turno_list')

class TurnoConfirmView(generic.View):
    def post(self, request, *args, **kwargs):
        turno = Turno.objects.get(pk=self.kwargs['pk'])
        turno.confirmado = True
        turno.save()
        return HttpResponseRedirect(reverse_lazy('turno_list'))

class ConsultaListView(generic.ListView):
    model = Consulta
    template_name = 'turno/consulta_list.html'

class ConsultaCreateView(generic.CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'turno/consulta_form.html'
    success_url = reverse_lazy('consulta_list')

class ConsultaUpdateView(generic.UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'turno/consulta_form.html'
    success_url = reverse_lazy('consulta_list')

class ConsultaDeleteView(generic.DeleteView):
    model = Consulta
    template_name = 'turno/consulta_confirm_delete.html'
    success_url = reverse_lazy('consulta_list')

