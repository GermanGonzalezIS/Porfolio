from django.urls import path
from . import views

app_name = 'defensoria_publica'

urlpatterns = [
   #URLS generales de licencia de conducir
    path('pedir-curp/',views.pedir_curp,name='pedir_curp'),
    path('verificar-curp/', views.verificar_curp, name='verificar_curp'),
    path('completar/<int:pk>', views.EditarDefensoriaPublica.as_view(), name='completar'),

    #URLS de licencia de conducir
    path('',views.ListaDefensoriaPublica.as_view(),name='lista'),
    path('nuevo/',views.NuevaDefensoriaPublica.as_view(),name='nuevo'),
    path('detalle/<int:pk>',views.DetalleDefensoriaPublica.as_view(),name='detalle'),
    path('editar/<int:pk>',views.EditarDefensoriaPublica.as_view(),name='editar'),
    path('eliminar/<int:pk>',views.EliminarDefensoriaPublica.as_view(),name='eliminar'),
]