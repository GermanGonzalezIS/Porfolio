from django.db import models

# Create your models here.


class Publicacion(models.Model):
    archivo = models.FileField(upload_to='publicaciones/', max_length=100)
    titulo = models.CharField("Título de la publicación", max_length=100)
    fecha_publicacion = models.DateField(
        'Fecha de Publicacion', auto_now_add=True)
    estatus = models.ForeignKey("catalogos.Estatus", verbose_name=(
        "Estatus"), on_delete=models.CASCADE, default=1)
    autor = models.ForeignKey("usuarios.Usuario",
                              verbose_name=("Usuario Postulante"),
                              on_delete=models.CASCADE)
