from django.urls import path

# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'expedicion_acta'

urlpatterns = [
    #URLS generales de licencia de conducir
    path('pedir-curp/',views.pedir_curp,name='pedir_curp'),
    path('verificar-curp/', views.verificar_curp, name='verificar_curp'),
    path('completar/<int:pk>', views.EditarExpedicionActa.as_view(), name='completar'),

    #URLS de licencia de conducir
    path('',views.ListaExpedicionActa.as_view(),name='lista'),
    path('nuevo/',views.NuevaExpedicionActa.as_view(),name='nuevo'),
    path('detalle/<int:pk>',views.DetalleExpedicionActa.as_view(),name='detalle'),
    path('editar/<int:pk>',views.EditarExpedicionActa.as_view(),name='editar'),
    path('eliminar/<int:pk>',views.EliminarExpedicionActa.as_view(),name='eliminar'),

]
