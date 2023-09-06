from django.test import TestCase
from publicaciones.models import Publicacion
from usuarios.models import Usuario
from catalogos.models import Estatus
from gestion_publicaciones.models import Revision, Estado


# Create your tests here.
class TestViews(TestCase):

    def test_insercion_revision_bd(self):

        estatus_nuevo = Estatus.objects.create(descripcion='En espera')
        estatus_nuevo.save()
        estado_nuevo = Estado.objects.create(descripcion='En espera')
        estado_nuevo.save()
        usuario = Usuario.objects.create(nombre='Germán',
                                         primer_apellido='González',
                                         segundo_apellido='Rodarte',
                                         correo_electronico='38192814@uaz.edu.mx',
                                         username='germanglez',
                                         password='german$123',)
        usuario.save()
        publicacion_nueva = Publicacion.objects.create(archivo='archivo_prueba.txt',
                                                       estatus=estatus_nuevo,
                                                       autor=usuario,
                                                       titulo="Prueba")
        revision = Revision.objects.create(publicacion=publicacion_nueva,
                                           usuario_revisor=usuario,
                                           archivo='archivo_prueba.txt',
                                           estado=estado_nuevo)
        self.assertEquals(revision,
                          Revision.objects.filter(id=revision.id).first())

    def test_insercion_revision_sin_usuario_revisor(self):

        estatus_nuevo = Estatus.objects.create(descripcion='en espera')
        estatus_nuevo.save()
        estado_nuevo = Estado.objects.create(descripcion='En espera')
        estado_nuevo.save()
        usuario = Usuario.objects.create(nombre='Germán',
                                         primer_apellido='González',
                                         segundo_apellido='Rodarte',
                                         correo_electronico='38192814@uaz.edu.mx',
                                         username='germanglez',
                                         password='german$123',)
        usuario.save()
        publicacion_nueva = Publicacion.objects.create(archivo='archivo_prueba.txt',
                                                       estatus=estatus_nuevo,
                                                       autor=usuario,
                                                       titulo="Prueba")
        revision = Revision.objects.create(publicacion=publicacion_nueva,
                                           usuario_revisor=None,
                                           archivo='archivo_prueba.txt',
                                           estado=estado_nuevo)
        self.assertEquals(revision,
                          Revision.objects.filter(id=revision.id).first())

    def test_insercion_revision_sin_archivo_revision(self):

        estatus_nuevo = Estatus.objects.create(descripcion='en espera')
        estatus_nuevo.save()
        estado_nuevo = Estado.objects.create(descripcion='En espera')
        estado_nuevo.save()
        usuario = Usuario.objects.create(nombre='Germán',
                                         primer_apellido='González',
                                         segundo_apellido='Rodarte',
                                         correo_electronico='38192814@uaz.edu.mx',
                                         username='germanglez',
                                         password='german$123',)
        usuario.save()
        publicacion_nueva = Publicacion.objects.create(archivo='archivo_prueba.txt',
                                                       estatus=estatus_nuevo,
                                                       autor=usuario,
                                                       titulo="Prueba")
        revision = Revision.objects.create(publicacion=publicacion_nueva,
                                           usuario_revisor=None,
                                           archivo=None,
                                           estado=estado_nuevo)
        self.assertEquals(revision,
                          Revision.objects.filter(id=revision.id).first())

    def insercion_estado(self):

        estado_nuevo = Estado.objects.create(descripcion='En espera')
        estado_nuevo.save()
        self.assertEquals(estado_nuevo,
                          Estado.objects.filter(id=estado_nuevo.id).first())

    def insercion_estado_sin_descricion(self):

        estado_nuevo = Estado.objects.create(descripcion=None)
        estado_nuevo.save()
        self.assertEquals(Estado.objects.all().count(), 0)
