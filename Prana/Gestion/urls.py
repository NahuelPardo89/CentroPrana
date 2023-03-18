from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/nuevo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),

    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/crear/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/editar/<int:pk>/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/eliminar/<int:pk>/', views.PacienteDeleteView.as_view(), name='paciente_delete'),

    path('medicos/', views.MedicoListView.as_view(), name='medico_list'),
    path('medicos/nuevo/', views.MedicoCreateView.as_view(), name='medico_create'),
    path('medicos/editar/<int:pk>/', views.MedicoUpdateView.as_view(), name='medico_update'),
    path('medicos/eliminar/<int:pk>/', views.MedicoDeleteView.as_view(), name='medico_delete'),
    path('medicos/<int:pk>/precios/', views.MedicoObraSocialListView.as_view(), name='medico_precioconsulta_list'),
    path('medicos/<int:pk>/precios/agregar/', views.PrecioConsultaCreateView.as_view(), name='medico_precioconsulta_create'),
    path('medicos/<int:medico_pk>/precios/<int:pk>/editar/', views.PrecioConsultaUpdateView.as_view(), name='medico_precioconsulta_update'),
    path('medicos/<int:medico_pk>/precios/<int:pk>/eliminar/', views.PrecioConsultaDeleteView.as_view(), name='medico_precioconsulta_delete'),

    path('secretarias/', views.SecretariaListView.as_view(), name='secretaria_list'),
    path('secretarias/nuevo/', views.SecretariaCreateView.as_view(), name='secretaria_create'),
    path('secretarias/editar/<int:pk>/', views.SecretariaUpdateView.as_view(), name='secretaria_update'),
    path('secretarias/eliminar/<int:pk>/', views.SecretariaDeleteView.as_view(), name='secretaria_delete'),

    path('obra_social/', views.ObraSocialListView.as_view(), name='obra_social_list'),
    path('obra_social/create/', views.ObraSocialCreateView.as_view(), name='obra_social_create'),
    path('obra_social/update/<int:pk>/', views.ObraSocialUpdateView.as_view(), name='obra_social_update'),
    path('obra_social/delete/<int:pk>/', views.ObraSocialDeleteView.as_view(), name='obra_social_delete'),

    path('especialidad_medica/', views.EspecialidadMedicaListView.as_view(), name='especialidad_medica_list'),
    path('especialidad_medica/create/', views.EspecialidadMedicaCreateView.as_view(), name='especialidad_medica_create'),
    path('especialidad_medica/update/<int:pk>/', views.EspecialidadMedicaUpdateView.as_view(), name='especialidad_medica_update'),
    path('especialidad_medica/delete/<int:pk>/', views.EspecialidadMedicaDeleteView.as_view(), name='especialidad_medica_delete'),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]
