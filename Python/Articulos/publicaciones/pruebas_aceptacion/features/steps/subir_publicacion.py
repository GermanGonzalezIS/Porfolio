import time
from behave import given, when, then


@given(u'que me encuentro logueado en el sistema como usuario postulante')
def step_impl(context):
    login(context)


@given(u'me dirijo a la pantalla de inicio del sistema en la dirección "{url}"')
def step_impl(context, url):
    context.driver.get(f"{context.url}")
    time.sleep(1)


@when(u'me dirijo a la pantalla de inicio del sistema en la dirección "{url}"')
def step_impl(context, url):
    context.driver.get(f"{context.url}")
    time.sleep(1)


@given(u'hago clic en la pestaña "Mis publicaciones"')
def step_impl(context):
    context.driver.find_element_by_id('id_mis_publicaciones').click()
    time.sleep(1)


@given(u'puedo ver el encabezado "{encabezado}"')
def step_impl(context, encabezado):
    respuesta = context.driver.find_element_by_id(
        'titulo_mis_publicaciones').text
    assert encabezado in respuesta, f"esperado es {encabezado} y obtenido es {respuesta}"
    time.sleep(1)


@given(u'hago clic en el enlace "Nueva Publicación"')
def step_impl(context):
    context.driver.find_element_by_id('nueva_publicacion').click()
    time.sleep(1)


@given(u'hago clic en el botón "Elegir archivo" y selecciono el archivo con la ruta "{ruta}"')
def step_impl(context, ruta):
    context.driver.find_element_by_id('id_archivo').send_keys(ruta)
    time.sleep(1)


@given(u'introduzco el título "{titulo}" en el campo designado')
def step_impl(context, titulo):
    context.driver.find_element_by_id('id_titulo').send_keys(titulo)
    time.sleep(1)


@when(u'doy click en el botón "Enviar archivo a revisión"')
def step_impl(context):
    context.driver.find_element_by_id('submit').click()
    time.sleep(1)


@then(u'recibo el mensaje "{mensaje_exito}".')
def step_impl(context, mensaje_exito):
    mensaje = context.driver.find_element_by_id('swal2-title').text
    assert mensaje_exito in mensaje, f"esperado es {mensaje_exito} y obtenido es {mensaje}"
    time.sleep(1)


@given(u'que no me encuentro logueado en el sistema como usuario postulante')
def step_impl(context):
    # context.driver.get(f"{context.url}{'admin/logout'}")
    login_no_postulante(context)
    time.sleep(1)


@when(u'hago clic en la pestaña "Publicaciones"')
def step_impl(context):
    context.driver.find_element_by_id('gestor_publicaciones').click()
    time.sleep(1)


@when(u'me dirijo a la dirección "{url}"')
def step_impl(context, url):
    context.driver.get(url)
    time.sleep(1)


@then(u'puedo ver el mensaje "Lo sentimos, tu cuenta de usuario no tiene acciones disponibles"')
def step_impl(context):
    mensaje_excepcion = "Lo sentimos, tu cuenta de usuario no tiene acciones disponibles"
    mensaje = context.driver.find_element_by_id('id_no_hay_acciones').text
    assert mensaje_excepcion in mensaje, f"esperado es {mensaje_excepcion} y obtenido es {mensaje}"
    time.sleep(1)


@then(u'puedo ver el mensaje "Ups! Esta página no está disponible"')
def step_impl(context):
    mensaje_excepcion = "Ups! Esta página no está disponible"
    mensaje = context.driver.find_element_by_id('id_403').text
    assert mensaje_excepcion in mensaje, f"esperado es {mensaje_excepcion} y obtenido es {mensaje}"
    time.sleep(2)


def login(context):
    context.driver.get(f"{context.url}{'usuarios/login'}")
    context.driver.find_element_by_id('id_username').send_keys('autor')
    context.driver.find_element_by_id('id_password').send_keys('temporal2019')
    context.driver.find_element_by_xpath(
        '//*[@id="layoutAuthentication_content"]/main/div/div/div/div/div[2]/form/div[3]/button').click()


def login_no_postulante(context):
    context.driver.get(f"{context.url}{'usuarios/login'}")
    context.driver.find_element_by_id('id_username').send_keys('no_postulante')
    context.driver.find_element_by_id('id_password').send_keys('temporal2019')
    context.driver.find_element_by_xpath(
        '//*[@id="layoutAuthentication_content"]/main/div/div/div/div/div[2]/form/div[3]/button').click()
