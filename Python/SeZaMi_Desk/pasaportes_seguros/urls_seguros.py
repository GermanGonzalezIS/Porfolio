from django.urls import path
from . import views_seguros

app_name = 'seguros'

urlpatterns = [
    path('lista/', views_seguros.SegurosList.as_view(), name = 'lista'),
    path('pedir-curp/',views_seguros.pedir_curp,name='pedir_curp'),
    path("verificar-curp/", views_seguros.verificar_curp, name="verificar_curp"),
    path("completar/<int:pk>", views_seguros.SeguroActualizar.as_view(), name="completar"),
    path("detalle/<int:pk>", views_seguros.SeguroDetalle.as_view(), name="detalle"),
    path("eliminar/<int:pk>", views_seguros.SeguroEliminar.as_view(), name="eliminar"),
    path('generar-curp/',views_seguros.generar_curp,name='generar_curp'),
]