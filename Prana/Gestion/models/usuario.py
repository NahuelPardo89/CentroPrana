# models/usuario.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.db import models

class UsuarioManager(BaseUserManager):
    def _create_user(self, dni, password, is_staff, is_superuser, **extra_fields):
        if not dni:
            raise ValueError('El DNI es obligatorio.')

        nombre = extra_fields.get('nombre')
        apellido = extra_fields.get('apellido')
        email = extra_fields.get('email')
        telefono = extra_fields.get('telefono')
        if not nombre:
            raise ValueError('El nombre es obligatorio.')
        if not apellido:
            raise ValueError('El apellido es obligatorio.')
        if not email:
            raise ValueError('El email es obligatorio.')

        user = self.model(
            dni=dni,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, dni, password=None, **extra_fields):
        return self._create_user(dni, password, False, False, **extra_fields)

    def create_superuser(self, dni, password=None, **extra_fields):
        return self._create_user(dni, password, True, True, **extra_fields)

class Usuario(AbstractBaseUser):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name='grupos',
        blank=True,
        help_text='Los grupos a los que pertenece el usuario.',
        related_name='user_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='permisos',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        related_name='user_set'
    )

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email', 'telefono']

    objects = UsuarioManager()

    def get_full_name(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def get_short_name(self):
        return self.nombre

    @property
    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def has_perm(self, perm, obj=None):
        """
        Determina si el usuario tiene un permiso específico.
        """
        if self.is_superuser:
            return True

        if self.is_staff:
            return perm in self.get_all_permissions()

        return perm in self.get_group_permissions()

    def has_module_perms(self, app_label):
        """
        Determina si el usuario tiene permisos para el módulo de la aplicación especificada.
        """
        if self.is_superuser:
            return True

        if self.is_staff:
            for perm in self.get_all_permissions():
                if perm.startswith(app_label):
                    return True
            return False

        for perm in self.get_group_permissions():
            if perm.startswith(app_label):
                return True

        return False

    def get_group_permissions(self):
        """
        Obtiene los permisos de los grupos a los que pertenece el usuario.
        """
        permissions = set()
        for group in self.groups.all():
            permissions.update(group.permissions.values_list('codename', flat=True))
        return permissions

    def get_all_permissions(self):
        """
        Obtiene todos los permisos del usuario, incluidos los permisos específicos y los permisos de grupo.
        """
        permissions = set(self.user_permissions.values_list('codename', flat=True))
        permissions.update(self.get_group_permissions())
        return permissions