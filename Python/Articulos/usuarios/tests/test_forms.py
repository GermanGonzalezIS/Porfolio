from django.test import TestCase
from usuarios.forms import UsuarioForm
from usuarios.models import Usuario


class TestFormUsuario(TestCase):
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
        self.data_usuario = {
            'nombre': 'Germán',
            'primer_apellido': 'González',
            'segundo_apellido': '',
            'correo_electronico': '38192814@uaz.edu.mx',
            'username': 'germanglez',
            'password': 'german$123',
        }

    def test_usuario_form_es_valido(self):

        form = UsuarioForm(self.data_usuario)
        self.assertTrue(form.is_valid())

    def test_usuario_form_nombre_vacio(self):

        self.data_usuario['nombre'] = ''
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())

    def test_usuario_form_corre_es_invalido(self):

        self.data_usuario['correo_electronico'] = '38192814@'
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())

    def test_usuario_form_email_vacio_mensaje(self):

        self.data_usuario['correo_electronico'] = ''
        form = UsuarioForm(self.data_usuario)
        self.assertEqual(form.errors['correo_electronico'],
                         ['Este campo es obligatorio.'])

    def test_usuario_form_password_es_requerido(self):

        self.data_usuario['password'] = ''
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())

    def test_usuario_form_username_es_requerido(self):

        self.data_usuario['username'] = ''
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())

    def test_usuario_form_primer_apellido_es_requerido(self):

        self.data_usuario['primer_apellido'] = ''
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())

    def test_usuario_form_segundo_apellido_no_es_requerido(self):

        self.data_usuario['segundo_apellido'] = ''
        form = UsuarioForm(self.data_usuario)
        self.assertTrue(form.is_valid())

    def test_usuario_form_nombre_max_no_valido(self):

        self.data_usuario['nombre'] = 'German'*20
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())

    def test_usuario_form_primer_apellido_max_no_valido(self):

        self.data_usuario['primer_apellido'] = 'González'*20
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())

    def test_usuario_form_segundo_apellido_max_no_valido(self):

        self.data_usuario['segundo_apellido'] = 'Rodarte'*20
        form = UsuarioForm(self.data_usuario)
        self.assertFalse(form.is_valid())
