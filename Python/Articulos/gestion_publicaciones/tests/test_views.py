from django.test import TestCase
from django.urls import reverse
from publicaciones.models import Publicacion
from usuarios.models import Usuario
from catalogos.models import Estatus
from gestion_publicaciones.models import Estado, Revision


# Create your tests here.
class TestViews(TestCase):

    def crear_publicacion(self):
        estatus_nuevo = Estatus.objects.create(descripcion='En espera')
        estatus_nuevo.save()
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
        publicacion_nueva.save()

    def crear_publicacion_revision(self):

        self.crear_publicacion()
        self.crear_estados()
        estado_nuevo = Estado.objects.get(descripcion='En espera')
        revision = Revision.objects.create(publicacion=Publicacion.objects.all().first(),
                                           usuario_revisor=Usuario.objects.all().first(),
                                           archivo='archivo_prueba.txt',
                                           estado=estado_nuevo)
        revision.save()

    def crear_estados(self):
        estado_espera = Estado.objects.create(descripcion='En espera')
        estado_espera.save()
        estado_aceptar = Estado.objects.create(descripcion='Aceptada')
        estado_aceptar.save()
        estado_rechazar = Estado.objects.create(descripcion='Rechazada')
        estado_rechazar.save()

    def test_url_publicaciones_lista(self):

        response = self.client.get(
            '/gestion-publicaciones/lista-publicaciones')
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_publicaciones_lista(self):

        response = self.client.get(
            reverse('gestion_publicaciones:lista_publicaciones'))
        self.assertEqual(response.status_code, 200)

    def test_template_correcto_publicaciones_lista(self):

        response = self.client.get(
            '/gestion-publicaciones/lista-publicaciones')
        self.assertTemplateUsed(response, 'publicaciones_list.html')

    def test_envio_datos_url_publicaciones_lista(self):

        response = self.client.get(
            reverse('gestion_publicaciones:lista_publicaciones'))
        self.assertIn('object_list', response.context)

    def test_url_publicaciones_detalle(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/detalle-publicacion/' +
                                   str(publicacion.id))
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_publicacion_detalle(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get(reverse('gestion_publicaciones:detalle_publicacion',
                                           args=[str(publicacion.id)]))
        self.assertEqual(response.status_code, 200)

    def test_template_correcto_publicacion_detalle(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/detalle-publicacion/' +
                                   str(publicacion.id))
        self.assertTemplateUsed(response, 'publicacion_detail.html')

    def test_envio_datos_url_publicacion_detalle(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/detalle-publicacion/' +
                                   str(publicacion.id))
        self.assertIn('publicacion', response.context)

    def test_envio_datos_url_publicacion_revisiones_detalle(self):

        self.crear_publicacion_revision()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/detalle-publicacion/' +
                                   str(publicacion.id))
        self.assertIn('revisiones', response.context)

    def test_url_lista_revisores(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/asignar-revisores/' +
                                   str(publicacion.id))
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_lista_revisores(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get(reverse('gestion_publicaciones:asignar_revisores',
                                           args=[str(publicacion.id)]))
        self.assertEqual(response.status_code, 200)

    def test_template_correcto_lista_revisores(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/asignar-revisores/' +
                                   str(publicacion.id))
        self.assertTemplateUsed(response, 'revisores_list.html')

    def test_envio_datos_url_lista_revisores_publicacion(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/asignar-revisores/' +
                                   str(publicacion.id))
        self.assertIn('publicacion', response.context)

    def test_envio_datos_url_lista_revisores_revisores(self):

        self.crear_publicacion()
        publicacion = Publicacion.objects.all().first()
        response = self.client.get('/gestion-publicaciones/asignar-revisores/' +
                                   str(publicacion.id))
        self.assertIn('revisores', response.context)

    def test_url_cambiar_revisor(self):

        self.crear_publicacion_revision()
        response = self.client.get('/gestion-publicaciones/cambiar-revisor/' +
                                   str(Revision.objects.all().first().id))
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_cambiar_revisor(self):

        self.crear_publicacion_revision()
        response = self.client.get(reverse('gestion_publicaciones:cambiar_revisor',
                                           args=[str(Revision.objects.all().first().id)]))
        self.assertEqual(response.status_code, 200)

    def test_template_correcto_cambiar_revisor(self):

        self.crear_publicacion_revision()
        response = self.client.get(reverse('gestion_publicaciones:cambiar_revisor',
                                           args=[str(Revision.objects.all().first().id)]))
        self.assertTemplateUsed(response, 'asignar_nuevo_revisor.html')

    def test_envio_datos_url_cambiar_revisor_revision(self):

        self.crear_publicacion_revision()
        response = self.client.get(reverse('gestion_publicaciones:cambiar_revisor',
                                           args=[str(Revision.objects.all().first().id)]))
        self.assertIn('revision', response.context)

    def test_envio_datos_url_cambiar_revisor_publicacion(self):

        self.crear_publicacion_revision()
        response = self.client.get(reverse('gestion_publicaciones:cambiar_revisor',
                                           args=[str(Revision.objects.all().first().id)]))
        self.assertIn('publicacion', response.context)

    def test_envio_datos_url_cambiar_revisor_lista_usuarios_disponibles(self):

        self.crear_publicacion_revision()
        response = self.client.get(reverse('gestion_publicaciones:cambiar_revisor',
                                           args=[str(Revision.objects.all().first().id)]))
        self.assertIn('usuarios_disponibles', response.context)

    def test_url_asignar_revisor(self):

        self.crear_publicacion()
        self.crear_estados()
        id_usuario = str(Usuario.objects.all().first().id)
        data_asignar_revisores = {'publicacion': Publicacion.objects.all().first().id,
                                  id_usuario: 'Selected'}
        response = self.client.post('/gestion-publicaciones/agregar-revisores/',
                                    data=data_asignar_revisores)
        self.assertEqual(response.status_code, 302)

    def test_asignar_revisor_publicacion_no_existente(self):

        self.crear_publicacion()
        self.crear_estados()
        id_usuario = str(Usuario.objects.all().first().id)
        data_asignar_revisores = {'publicacion': 100,
                                  id_usuario: 'Selected'}
        response = self.client.post('/gestion-publicaciones/agregar-revisores/',
                                    data=data_asignar_revisores)
        self.assertEqual(response.status_code, 404)
