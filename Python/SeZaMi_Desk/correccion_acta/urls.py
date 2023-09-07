from django.urls import path

# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'correccion_acta'

urlpatterns = [
    #URLS generales de Ferias binacionales
    path('pedir-curp/',views.pedir_curp,name='pedir_curp'),
    path('verificar-curp/', views.verificar_curp, name='verificar_curp'),
    path('completar/<int:pk>', views.EditarCorreccionActa.as_view(), name='completar'),

    #URLS de Constancia de Estudios
    path('',views.ListaCorreccionActa.as_view(),name='lista'),
    path('nuevo/',views.NuevaCorreccionActa.as_view(),name='nuevo'),
    path('detalle/<str:pk>',views.DetalleCorreccionActa.as_view(),name='detalle'),
    path('editar/<str:pk>',views.EditarCorreccionActa.as_view(),name='editar'),
    path('eliminar/<str:pk>',views.EliminarCorreccionActa.as_view(),name='eliminar'),

]