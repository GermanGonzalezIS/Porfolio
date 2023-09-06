from behave import when, then, given
import time


# Nuevo usuario
@given(u'que ingreso al sistema con la dirección "{url}"')
def step_impl(context, url):

    context.driver.maximize_window()
    url_login = context.url+'usuarios/login'
    context.driver.get(url_login)
    time.sleep(2)
    context.driver.find_element_by_id("id_username").send_keys('admin')
    time.sleep(2)
    context.driver.find_element_by_id("id_password").send_keys('admin123')
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "//*[contains(text(), 'Ingresar')]")[0].click()
    time.sleep(2)
    context.driver.get(context.url+url)
    time.sleep(2)


@given(u'hago click en el botón "{texto_boton}"')
def step_impl(context, texto_boton):

    context.driver.find_element_by_link_text(texto_boton).click()
    time.sleep(2)


@given(u'capturo "{nombre}" en el nombre')
def step_impl(context, nombre):

    context.driver.find_element_by_id("id_nombre").clear()
    context.driver.find_element_by_id("id_nombre").send_keys(nombre)
    time.sleep(2)


@given(u'capturo "{apellido}" en el apellido')
def step_impl(context, apellido):

    context.driver.find_element_by_id("id_apellido").clear()
    context.driver.find_element_by_id("id_apellido").send_keys(apellido)
    time.sleep(2)


@given(u'capturo "{apellido}" en el segundo apellido')
def step_impl(context, apellido):

    context.driver.find_element_by_id("id_segundo_apellido").clear()
    context.driver.find_element_by_id(
        "id_segundo_apellido").send_keys(apellido)
    time.sleep(2)


@given(u'capturo "{username}" en el username')
def step_impl(context, username):

    context.driver.find_element_by_id("id_username").clear()
    context.driver.find_element_by_id("id_username").send_keys(username)
    time.sleep(2)


@given(u'capturo "{email}" en correo')
def step_impl(context, email):

    context.driver.find_element_by_id("id_email").clear()
    context.driver.find_element_by_id("id_email").send_keys(email)
    time.sleep(2)


@given(u'capturo "{password}" en el password')
def step_impl(context, password):

    context.driver.find_element_by_id("id_password").clear()
    context.driver.find_element_by_id("id_password").send_keys(password)
    time.sleep(2)


@when(u'presiono el botón "{boton}"')
def step_impl(context, boton):

    context.driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "//*[contains(text(), '"+boton+"')]")[0].click()
    time.sleep(2)


@then(u'puede ver al usuario "{usuario}" en la lista de usuarios')
def step_impl(context, usuario):

    context.test.assertIn(usuario, context.driver.page_source)
    time.sleep(2)


@then(u'puede ver el mensaje "{mensaje}" en la página')
def step_impl(context, mensaje):

    context.test.assertIn(mensaje, context.driver.page_source)
    time.sleep(2)


@then(u'sigo en la misma página con el título "{titulo}"')
def step_impl(context, titulo):

    respuesta = context.driver.find_element_by_xpath(
        '/html/body/div/div[2]/main/div/div[1]/div/div/h1')
    assert titulo == respuesta.text, f"esperado es {titulo} y obtenido es {respuesta.text}"
    time.sleep(2)


# Iniciar sesión
@given(u'capturo "{username}" en el nombre de usuario')
def step_impl(context, username):

    context.driver.find_element_by_id("id_username").send_keys(username)
    time.sleep(2)


@given(u'capturo "{password}" en contraseña')
def step_impl(context, password):

    context.driver.find_element_by_id("id_password").send_keys(password)
    time.sleep(2)


@then(u'puedo ver la página de "{pagina}"')
def step_impl(context, pagina):

    context.test.assertIn(pagina, context.driver.page_source)
    time.sleep(2)


@then(u'puedo ver la alerta "{alerta}" en la página')
def step_impl(context, alerta):

    context.test.assertIn(alerta, context.driver.page_source)
    time.sleep(2)


# Eliminar Usuario
@given(u'presiono el botón de eliminar correspondiente a un registro de la lista')
def step_impl(context):

    context.driver.find_element_by_xpath(
        '//*[@id="datatablesSimple"]/tbody/tr[1]/td[7]/button').click()
    time.sleep(2)


@given(u'presiono el botón "Sí, estoy seguro"')
def step_impl(context):

    context.driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[6]/button[1]').click()
    time.sleep(2)


@given(u'presiono el botón "Cancelar"')
def step_impl(context):

    context.driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[6]/button[3]').click()
    time.sleep(2)


# Modificar
@given(u'presiono el botón de modificar correspondiente a un registro de la lista')
def step_impl(context):

    context.driver.find_element_by_xpath(
        '/html/body/div/div[2]/main/div/div/div/div/div[2]/table/tbody/tr[1]/td[7]/a[2]').click()
    time.sleep(2)


@given(u'capturo "" en el nombre')
def step_impl(context):

    context.driver.find_element_by_id("id_nombre").clear()
    time.sleep(2)


@given(u'capturo "" en el apellido')
def step_impl(context):

    context.driver.find_element_by_id("id_apellido").clear()
    time.sleep(2)


@given(u'capturo "" en el username')
def step_impl(context):

    context.driver.find_element_by_id("id_username").clear()
    time.sleep(2)


# Detalle
@when(u'presiono el botón de ver correspondiente a un registro de la lista')
def step_impl(context):

    context.driver.find_element_by_xpath(
        '/html/body/div/div[2]/main/div/div/div/div/div[2]/table/tbody/tr[1]/td[7]/a[1]').click()
    time.sleep(2)


# Modificar permisos
@given(u'selecciono el permiso Administrador')
def step_impl(context):

    context.driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div[2]/div/form/div[1]/div[2]/label/span")[0].click()
    time.sleep(2)


@given(u'selecciono el permiso Gestor')
def step_impl(context):

    context.driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div[2]/div/form/div[2]/div[2]/label/span")[0].click()
    time.sleep(2)


@given(u'selecciono el permiso Postulante')
def step_impl(context):

    context.driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div[2]/div/form/div[3]/div[2]/label/span")[0].click()
    time.sleep(2)


@given(u'selecciono el permiso Revisor')
def step_impl(context):

    context.driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div[2]/div/form/div[4]/div[2]/label/span")[0].click()
    time.sleep(2)
