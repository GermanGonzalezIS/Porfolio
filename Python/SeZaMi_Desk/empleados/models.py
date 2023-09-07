from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField 

class Empleado(User):
    segundo_apellido = models.CharField('Segundo apellido',max_length=50)
    telefono = models.CharField('Teléfono',max_length=10,null=True)
    contra = models.CharField('Contraseña',max_length=50,default=None)
    grupo = models.ForeignKey("empleados.Grupo", verbose_name=("Grupo"), on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name+' '+self.last_name+' '+self.segundo_apellido

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

class Grupo(models.Model):
    grupo = models.CharField(max_length=50)

    def __str__(self):
        return self.grupo

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'