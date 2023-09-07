from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, BooleanField
from django.core.validators import RegexValidator

class Usuario(User):
    segundo_apellido = models.CharField('Segundo apellido',max_length=50)
    fecha_nacimiento = models.DateField()
    curp = models.CharField("CURP", primary_key = True, max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    entidad = models.ForeignKey("usuarios.Entidad_Federativa", verbose_name="Entidad Federativa", on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    super_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Entidad_Federativa(models.Model):
    clave = models.CharField('Clave',max_length=2)
    entidad = models.CharField('Entidad Federativa',max_length=50)

    def __str__(self):
        return self.entidad

