from django.urls import path

# Se importan las vistas a llamar en esta aplicación
# del proyecto 
from . import views

app_name = 'doble_nacionalidad'

urlpatterns = [
    #URLS de Doble nacionalidad
    path('',views.ListaDobleNacionalidad.as_view(),name='lista'),
    path('nuevo/',views.NuevaDobleNacionalidad.as_view(),name='nuevo'),
    # path('detalle/<str:pk>',views.DetalleDobleNacionalidad.as_view(),name='detalle'),
    # path('editar/<str:pk>',views.EditarDobleNacionalidad.as_view(),name='editar'),
    # path('eliminar/<str:pk>',views.EliminarDobleNacionalidad.as_view(),name='eliminar'),

]