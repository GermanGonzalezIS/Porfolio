from django.test import TestCase
from io import BytesIO
from publicaciones.forms import PublicacionForm
from django.core.files.uploadedfile import SimpleUploadedFile


class TestFormPublicacion(TestCase):

    # Probar que la form del modelo Publicación se
    # marca como inválida si falta una ruta de archivo
    def test_archivo_vacio_form(self):
        form = PublicacionForm(
            data={
                'titulo': 'Prueba'
            }
        )
        self.assertFalse(form.is_valid())

    # Probar que la form del modelo Publicación se
    # marca como inválida si falta un título de archivo
    def test_titulo_vacio_form(self):
        loaded_file = BytesIO(b"texto de prueba")
        loaded_file.name = 'archivo.txt'

        data = {
            'titulo': ''
        }
        form = PublicacionForm(data=data, files={'archivo': SimpleUploadedFile(
            loaded_file.name, loaded_file.read())})
        self.assertFalse(form.is_valid())

    # Probar que la form del modelo es válida si cuenta con los datos 'archivo' y 'título'
    def test_form_valida(self):
        loaded_file = BytesIO(b"texto de prueba")
        loaded_file.name = 'archivo.txt'

        data = {
            'titulo': 'Prueba'
        }
        form = PublicacionForm(data=data, files={'archivo': SimpleUploadedFile(
            loaded_file.name, loaded_file.read())})
        self.assertTrue(form.is_valid())

    # Probar que la form del modelo es inválida si el título supera los 100 caracteres
    def test_form_titulo_invalido(self):
        loaded_file = BytesIO(b"texto de prueba")
        loaded_file.name = 'archivo.txt'

        data = {
            'titulo': 'ysagsdyagsdhjasgdygacygcugadghsdhasgdhasgdhasgdhasgdhasghdasghdgashdgahsgdasgdhasgdhjgashdgashdghasgdhasgdhgashjdgsdasdiasdiashdihsauidhasuduasgduasgdasgudgasuodhasjhdjashdjkashdjkasgdgashdgashdghjasgdhjasgdhaagjsgfjcvsgjs'
        }
        form = PublicacionForm(data=data, files={'archivo': SimpleUploadedFile(
            loaded_file.name, loaded_file.read())})
        self.assertFalse(form.is_valid())

    # Probar que la form del modelo es inválida si el nombre/ruta del archivo supera los 100 caracteres
    def test_form_ruta_invalida(self):
        loaded_file = BytesIO(b"texto de prueba")
        loaded_file.name = 'ysagsdyagsdhjasgdygacygcugadghsdhasgdhasgdhasgdhasgdhasghdasghdgashdgahsgdasgdhasgdhjgashdgashdghasgdhasgdhgashjdgsdasdiasdiashdihsauidhasuduasgduasgdasgudgasuodhasjhdjashdjkashdjkasgdgashdgashdghjasgdhjasgdhaagjsgfjcvsgjs.txt'

        data = {
            'titulo': 'prueba'
        }
        form = PublicacionForm(data=data, files={'archivo': SimpleUploadedFile(
            loaded_file.name, loaded_file.read())})
        self.assertFalse(form.is_valid())
