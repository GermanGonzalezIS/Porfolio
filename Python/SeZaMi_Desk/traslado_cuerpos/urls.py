from django.urls import path
from . import views

app_name = 'traslado_cuerpos'

urlpatterns = [
    path('', views.ListaTrasladoCuerpo.as_view(), name='lista'),
    path('editar/<str:pk>', views.EditarTrasladoCuerpo.as_view(), name='editar'),
    path('nuevo/', views.AgregarTrasladoCuerpo.as_view(), name='nuevo'),
    path('detalle/<str:pk>', views.DetalleTrasladoCuerpo.as_view(), name='detalle'),
    path('eliminar/<str:pk>',views.EliminarTrasladoCuerpo.as_view(),name='eliminar'),
]