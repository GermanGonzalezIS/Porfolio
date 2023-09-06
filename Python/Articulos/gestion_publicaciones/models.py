from django.db import models


# Create your models here.
class Revision(models.Model):
    publicacion = models.ForeignKey("publicaciones.Publicacion",
                                    verbose_name=("Publicación"),
                                    on_delete=models.CASCADE,
                                    null=False)
    usuario_revisor = models.ForeignKey("usuarios.Usuario",
                                        verbose_name=("Usuario Revisor"),
                                        on_delete=models.CASCADE,
                                        null=True)
    archivo = models.FileField(upload_to='revisiones/',
                               max_length=100,
                               null=True, blank=True)
    estado = models.ForeignKey("gestion_publicaciones.Estado",
                               verbose_name="Estado",
                               on_delete=models.CASCADE,
                               null=False)


class Estado(models.Model):
    descripcion = models.CharField("Estado de la solicitud", max_length=100)

    def __str__(self):
        return self.descripcion
