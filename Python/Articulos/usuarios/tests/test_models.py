from django.test import TestCase
from django.core.exceptions import ValidationError
from usuarios.models import Usuario


# Create your tests here.
class TestModels(TestCase):

    def setUp(self,
              nombre='Germán',
              primer_apellido='González',
              segundo_apellido='',
              correo_electronico='38192814@uaz.edu.mx',
              username='germanglez',
              password='german$123',
              ):

        self.usuario = Usuario(
            nombre=nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            correo_electronico=correo_electronico,
            username=username,
            password=password
        )

    def test_regresa_objeto_usuario(self):

        self.usuario.full_clean()
        self.usuario.save()
        self.assertEqual(Usuario.objects.first().__str__(),
                         self.usuario.__str__())

    def test_nombre_es_requerido(self):

        usuario = Usuario(
            primer_apellido='González',
            segundo_apellido='',
            correo_electronico='38192814@uaz.edu.mx',
            username='germanglez',
            password='german$123',
        )
        with self.assertRaises(ValidationError):
            usuario.full_clean()

    def test_username_no_acepta_espacios(self):

        self.usuario.username = 'german glez'
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

    def test_usuario_duplicado(self):

        self.usuario.save()
        usuario2 = Usuario(
            nombre='Germán',
            primer_apellido='González',
            segundo_apellido='',
            correo_electronico='38192817@uaz.edu.mx',
            username='germanglez',
            password='german$123'
        )
        try:
            usuario2.full_clean()
        except ValidationError as ex:
            msg = str(ex.message_dict['username'][0])
            self.assertEqual(msg, 'Ya existe un usuario con ese nombre.')

    def test_correo_es_requerido(self):

        usuario = Usuario(
            nombre='Germán',
            primer_apellido='González',
            segundo_apellido='',
            username='germanglez',
            password='german$123'
        )
        self.usuario = usuario
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

    def test_correo_incorrecto(self):

        self.usuario.correo_electronico = '38192817@'
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

    def test_correo_incorrecto_con_espacios(self):

        self.usuario.email = '38192817@uaz .edu.mx'
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

    def test_correo_incorrecto_min_caracteres(self):

        self.usuario.correo_electronico = '38@'
        with self.assertRaises(ValidationError):
            self.usuario.full_clean()

    def test_email_duplicado(self):

        self.usuario.save()
        usuario2 = Usuario(
            nombre='Germán',
            primer_apellido='González',
            segundo_apellido='',
            correo_electronico='38192814@uaz.edu.mx',
            username='germanglez2',
            password='german$1234'
        )
        try:
            usuario2.full_clean()
        except ValidationError as ex:
            msg = str(ex.message_dict['correo_electronico'][0])
            self.assertEqual(msg,
                             'Ya existe un/a Usuario con este/a Correo electronico.')

    def test_password_es_requerido(self):

        usuario = Usuario(
            nombre='Germán',
            primer_apellido='González',
            segundo_apellido='',
            correo_electronico='38192814@uaz.edu.mx',
            username='germanglez'
        )
        with self.assertRaises(ValidationError):
            usuario.full_clean()
