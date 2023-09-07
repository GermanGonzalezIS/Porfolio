from django.urls import path
from . import views

app_name = 'visas'

urlpatterns = [
    path('',views.ListaVisa.as_view(),name='lista'),
    path('nueva/',views.NuevaVisa.as_view(),name='nueva'),
    path('detalle/<int:pk>',views.DetalleVisa.as_view(),name='detalle'),
    path('editar/<int:pk>',views.EditarVisa.as_view(),name='editar'),
    path('eliminar/<int:pk>',views.EliminarVisa.as_view(),name='eliminar'),
]