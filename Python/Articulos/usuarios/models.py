from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, EmailField
from django.core.validators import validate_email


class Usuario(User):

    nombre = CharField(blank=False, max_length=100)
    primer_apellido = CharField(blank=False, max_length=100)
    segundo_apellido = CharField(max_length=100, blank=True)
    correo_electronico = EmailField(blank=False,
                                    unique=True, validators=[validate_email, ])

    def __str__(self):
        return self.nombre+' '+self.primer_apellido

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
