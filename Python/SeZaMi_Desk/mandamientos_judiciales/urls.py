from django.urls import path

# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'mandamientos_judiciales'

urlpatterns = [
    #URLS generales de mandamientos judiciales
    path('pedir-curp/',views.pedir_curp,name='pedir_curp'),
    path('verificar-curp/', views.verificar_curp, name='verificar_curp'),
    path('completar/<int:pk>', views.EditarMandamientosJudiciales.as_view(), name='completar'),

    # URLS de Mandamientos judiciales
    path('',views.ListaMandamientosJudiciales.as_view(),name='lista'),
    path('nuevo/',views.NuevaMandamientosJudiciales.as_view(),name='nuevo'),
    path('detalle/<int:pk>',views.DetalleMandamientosJudiciales.as_view(),name='detalle'),
    path('editar/<int:pk>',views.EditarMandamientosJudiciales.as_view(),name='editar'),
    path('eliminar/<int:pk>',views.EliminarMandamientosJudiciales.as_view(),name='eliminar'),

]
