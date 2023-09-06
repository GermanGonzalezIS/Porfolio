from django.db import models

# Create your models here.


class Estatus(models.Model):
    descripcion = models.CharField("Estatus de la publicación", max_length=100)

    def __str__(self):
        return self.descripcion
