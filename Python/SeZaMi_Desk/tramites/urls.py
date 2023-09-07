from django.urls import path
# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'tramites'

urlpatterns = [
    path('lista/',views.TramiteList.as_view(), name = 'lista_tramite'),
    path('pedir-curp',views.pedir_curp,name='pedir_curp'),
    path('editar/<int:pk>',views.TramiteEditar.as_view(),name='editar'),
    path('actualizar-estatus/<int:pk>',views.actualizar_tramite,name='actualizar'),
    path('actualizar/<int:pk>',views.guardar_acualizacion,name='guardar_acualizacion'),
    path('eliminar/<int:pk>',views.TramiteEliminar.as_view(),name='eliminar'),
    path('ferias-binacionales/',views.ferias_binacionales,name='ferias_binacionales'),
]

