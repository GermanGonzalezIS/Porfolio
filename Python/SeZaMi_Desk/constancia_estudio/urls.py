from django.urls import path

# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'constancia_estudios'

urlpatterns = [
    #URLS generales de Ferias binacionales
    path('pedir-curp/',views.pedir_curp,name='pedir_curp'),
    path('verificar-curp/', views.verificar_curp, name='verificar_curp'),
    path('completar/<int:pk>', views.EditarConstanciaEstudio.as_view(), name='completar'),

    #URLS de Constancia de Estudios
    path('',views.ConstanciaEstudioList.as_view(),name='lista'),
    path('nuevo/',views.NuevaConstanciaEstudio.as_view(),name='nuevo'),
    path('detalle/<str:pk>',views.DetalleConstanciaEstudio.as_view(),name='detalle'),
    path('editar/<str:pk>',views.EditarConstanciaEstudio.as_view(),name='editar'),
    path('eliminar/<str:pk>',views.EliminarConstanciaEstudio.as_view(),name='eliminar'),

]