from django.test import TestCase
from publicaciones.models import Publicacion
from catalogos.models import Estatus
from django.contrib.auth.models import User

from usuarios.models import Usuario


# Create your tests here.
class TestModels(TestCase):

    # Probar la inserción de una publicación a la base de datos
    def test_insercion_publicacion_bd(self):
        publicacion = Publicacion.objects.create(
            archivo='archivo_prueba.txt',
            estatus=Estatus.objects.create(
                descripcion='en espera'),  # Estatus pendiente
            autor=Usuario.objects.create(
                username='autor_prueba', password='contra123'),
            titulo="Prueba"
        )
        self.assertEquals(publicacion, Publicacion.objects.filter(
            id=publicacion.id).first())

    # Probar la inserción de un estatus a la base de datos
    def test_insercion_estatus_bd(self):
        estatus = Estatus.objects.create(
            descripcion='Pendiente',
        )
        self.assertEquals(
            estatus, Estatus.objects.filter(id=estatus.id).first())
