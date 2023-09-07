from django.urls import path
# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'catalogos'

urlpatterns = [
    path('index/', views.CatalogoGeneral.as_view(), name = 'index'),
    path('municipios/',views.obtener_municipios,name='municipios'),
    path('localidades/',views.obtener_localidades,name='localidades'),
    path('asentamientos/',views.obtener_asentamientos,name='asentamientos'),
]

