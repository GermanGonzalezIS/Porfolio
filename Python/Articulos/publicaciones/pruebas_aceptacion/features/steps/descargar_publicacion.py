import time
from behave import given, when, then
import os.path


@given(u'que ya me encuentro logueado como usuario revisor')
def step_impl(context):
    login(context)
    time.sleep(1)


@given(u'me dirijo a la página de inicio del sistema')
def step_impl(context):
    context.driver.get(f"{context.url}")
    time.sleep(1)


@given(u'doy clic en la pestaña "Mis revisiones"')
def step_impl(context):
    context.driver.find_element_by_id('id_mis_revisiones').click()
    time.sleep(1)


@given(u'doy clic en el botón "Ver" una publicación')
def step_impl(context):
    context.driver.find_element_by_id('id_ver').click()
    time.sleep(1)


@when(u'doy clic en el botón "Descargar publicación"')
def step_impl(context):
    context.driver.find_element_by_id('id_descargar').click()
    time.sleep(1)


@then(u'puedo encontrar el archivo en la carpeta de descargas')
def step_impl(context):
    time.sleep(4)
    assert str(os.path.exists(
        'C:/Users/alejv/Downloads/publicaciones_UseCaseTesting_Sy30bt2.pdf')) in "True"


@given(u'que NO me encuentro logueado en el sistema como usuario revisor')
def step_impl(context):
    login_autor(context)
    time.sleep(1)


def login(context):
    context.driver.get(f"{context.url}{'usuarios/login'}")
    context.driver.find_element_by_id('id_username').send_keys('revisor')
    context.driver.find_element_by_id('id_password').send_keys('temporal2019')
    context.driver.find_element_by_xpath(
        '//*[@id="layoutAuthentication_content"]/main/div/div/div/div/div[2]/form/div[3]/button').click()


def login_autor(context):
    context.driver.get(f"{context.url}{'usuarios/login'}")
    context.driver.find_element_by_id('id_username').send_keys('autor')
    context.driver.find_element_by_id('id_password').send_keys('temporal2019')
    context.driver.find_element_by_xpath(
        '//*[@id="layoutAuthentication_content"]/main/div/div/div/div/div[2]/form/div[3]/button').click()
