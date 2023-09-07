from django.urls import path
from . import views_pasaportes

app_name = 'pasaportes'

urlpatterns = [
    path('lista/', views_pasaportes.PasaportesList.as_view(), name = 'lista'),
    path("nuevo/", views_pasaportes.PasaporteNuevo.as_view(), name="nuevo"),
    path("completar/<int:pk>", views_pasaportes.PasaporteActualizar.as_view(), name="completar"),
    path('pedir-curp/',views_pasaportes.pedir_curp,name='pedir_curp'),
    path("verificar-curp/", views_pasaportes.verificar_curp, name="verificar_curp"),
    path("detalle/<int:pk>", views_pasaportes.PasaporteDetalle.as_view(), name="detalle"),
    path("eliminar/<int:pk>", views_pasaportes.PasaporteEliminar.as_view(), name="eliminar"),
    path("inicio/", views_pasaportes.inicio_servicio, name="inicio"),
    path('generar-curp/',views_pasaportes.generar_curp,name='generar_curp'),
]