from behave import when, then, given
import time


# Ver estatus
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


@given(u'presiono el botón ver de la primera publicación de la lista')
def step_impl(context):

    context.driver.find_element_by_xpath(
        '/html/body/div/div[2]/main/div/div/div/div/div[2]/table/tbody/tr[1]/td[6]/a').click()
    time.sleep(2)


@then(u'puedo ver en la descripción de la publicación su estatus')
def step_impl(context):

    context.test.assertIn('Estatus', context.driver.page_source)
    time.sleep(2)


# Asignar revisores
@given(u'presiono el botón "{boton}"')
def step_impl(context, boton):

    context.driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    context.driver.find_elements_by_xpath(
        "//*[contains(text(), '"+boton+"')]")[0].click()
    time.sleep(2)


@when(u'presiono el botón "{boton}"')
def step_impl(context, boton):

    context.driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    context.driver.find_elements_by_xpath(
        "//*[contains(text(), '"+boton+"')]")[0].click()
    time.sleep(2)


@given(u'selecciono los primeros 3 revisores de la lista')
def step_impl(context):

    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[1]/td[7]/div/input")[0].click()
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[2]/td[7]/div/input")[0].click()
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[3]/td[7]/div/input")[0].click()
    time.sleep(2)


@when(u'selecciono los primeros 3 revisores de la lista')
def step_impl(context):

    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[1]/td[7]/div/input")[0].click()
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[2]/td[7]/div/input")[0].click()
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[3]/td[7]/div/input")[0].click()
    time.sleep(2)


@when(u'selecciono los primeros 2 revisores de la lista')
def step_impl(context):

    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[1]/td[7]/div/input")[0].click()
    time.sleep(2)
    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[2]/td[7]/div/input")[0].click()
    time.sleep(2)


@then(u'puedo ver a los 3 revisores en el detalle de la publicación')
def step_impl(context):

    rows = context.driver.find_elements_by_tag_name('tr')
    context.test.assertEqual(len(rows), 4)


@then(u'puedo ver la página "{titulo}"')
def step_impl(context, titulo):

    context.test.assertIn(titulo, context.driver.page_source)
    time.sleep(2)


@then(u'no puedo seleccionar el 4 revisor')
def step_impl(context):

    ele = context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[4]/td[7]/div/input")[0]
    time.sleep(2)
    ele.click()
    time.sleep(2)
    context.test.assertEqual(ele.is_selected(), False)


@then(u'no puedo presionar el botón Aceptar')
def step_impl(context):

    ele = context.driver.find_elements_by_id('id_aceptar')[0]
    time.sleep(2)
    context.test.assertEqual(ele.is_enabled(), False)


# Cambiar revisor
@given(u'selecciono el primer revisor de la lista')
def step_impl(context):

    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[1]/td[7]/div/input")[0].click()
    time.sleep(2)


@given(u'presiono el botón ver de la segunda publicación de la lista')
def step_impl(context):

    context.driver.find_element_by_xpath(
        '/html/body/div/div[2]/main/div/div/div/div/div[2]/table/tbody/tr[2]/td[6]/a').click()
    time.sleep(2)


@then(u'no puedo seleccionar el segundo revisor')
def step_impl(context):

    ele = context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[2]/td[7]/div/input")[0]
    time.sleep(2)
    ele.click()
    time.sleep(2)
    context.test.assertEqual(ele.is_selected(), False)


@when(u'selecciono el primer revisor de la lista')
def step_impl(context):

    context.driver.find_elements_by_xpath(
        "/html/body/div/div[2]/main/div/div/div/form/table/tbody/tr[1]/td[7]/div/input")[0].click()
    time.sleep(2)


@then(u'puedo ver el mensaje "{mensaje}"')
def step_impl(context, mensaje):

    context.test.assertIn(mensaje, context.driver.page_source)
    time.sleep(2)
