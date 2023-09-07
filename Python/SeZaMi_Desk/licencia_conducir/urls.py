from django.urls import path

# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'licencia_conducir'

urlpatterns = [
    #URLS generales de licencia de conducir
    path('pedir-curp/',views.pedir_curp,name='pedir_curp'),
    path('verificar-curp/', views.verificar_curp, name='verificar_curp'),
    path('completar/<int:pk>', views.EditarLicenciaConducir.as_view(), name='completar'),

    #URLS de licencia de conducir
    path('',views.ListaLicenciaConducir.as_view(),name='lista'),
    path('nuevo/',views.NuevaLicenciaConducir.as_view(),name='nuevo'),
    path('detalle/<int:pk>',views.DetalleLicenciaConducir.as_view(),name='detalle'),
    path('editar/<int:pk>',views.EditarLicenciaConducir.as_view(),name='editar'),
    path('eliminar/<int:pk>',views.EliminarLicenciaConducir.as_view(),name='eliminar'),

]
