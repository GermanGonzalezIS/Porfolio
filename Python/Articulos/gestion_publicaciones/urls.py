from django.urls import path
from . import views

app_name = 'gestion_publicaciones'

urlpatterns = [
    path('lista-publicaciones', views.PublicacionesList.as_view(),
         name='lista_publicaciones'),
    path('detalle-publicacion/<int:pk>', views.detalle_publicacion,
         name='detalle_publicacion'),
    path('asignar-revisores/<int:pk>', views.mostrar_lista_revisores,
         name='asignar_revisores'),
    path('agregar-revisores/', views.asignar_revisores,
         name='agregar_revisores'),
    path('cambiar-estado-solicitud/<slug:rid64>/<slug:token>/<slug:estado>',
         views.CambiarEstadoSolicitud.as_view(),
         name='cambiar_estado_solicitud'),
    path('enviar-recordatorio/<int:pk>',
         views.recordatorio,
         name='enviar_recordatorio'),
    path('cambiar-revisor/<int:pk>',
         views.cambiar_revisor,
         name='cambiar_revisor'),
]
