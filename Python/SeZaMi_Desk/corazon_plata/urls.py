from django.urls import path 
from . import views

app_name = 'corazon_plata'

urlpatterns = [
    # path('', views.CorazonPlataList.as_view(), name="lista"),
    # path("detalle/<int:pk>", views.CorazonPlataDetalle.as_view(), name="detalle"),
    path('', views.GrupoVisaList.as_view(), name="lista"), # lista de grupos de corazón de plata
    path("detalle_grupo/<int:pk>", views.GrupoVisaDetalle.as_view(), name="detalle_grupo"),
    path("detalle/<int:pk>", views.CorazonPlataDetalle.as_view(), name="detalle"),
    path("actualizar_grupo/<int:pk>", views.GrupoVisaActualizar.as_view(), name="actualizar_grupo"),
    path("eliminar_grupo/<int:pk>", views.GrupoVisaEliminar.as_view(), name="eliminar_grupo"),
    path("eliminar/<int:pk>", views.CorazonPlataEliminar.as_view(), name="eliminar"),
    path("nuevo/", views.CorazonPlataNuevo.as_view(), name="nuevo"),
    path("completar/<int:pk>", views.CorazonPlataActualizar.as_view(), name="completar"),
    path("nuevo_grupo/", views.GrupoVisaNuevo.as_view(), name="nuevo_grupo"),
    path("nuevo_tramite/", views.nuevo_tramite, name="nuevo_tramite"),
]
