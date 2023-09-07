from django.urls import path
from . import views

app_name = 'localizacion_personas'

urlpatterns = [
    path('lista/', views.ListaPersonasDesaparecidas.as_view(), name='lista'),
    path('editar/<str:pk>', views.EditarPersonaDesaparecida.as_view(), name='editar'),
    path('nuevo/', views.AgregarPersonaDesaparecida.as_view(), name='nuevo'),
    path('detalle/<str:pk>', views.DetallePersonaDesaparecida.as_view(), name='detalle'),
    path('eliminar/<str:pk>',views.EliminarPersonaDesaparecida.as_view(), name='eliminar'),
]