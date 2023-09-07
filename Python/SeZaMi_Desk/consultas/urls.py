from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
    path('', views.index, name='index'),
    path('lista-tramites',views.lista,name='lista'),
    path('detalle/<int:pk>', views.detalle, name='detalle'),
    path('detalle-solicitud/', views.detalleSolicitud, name='detalle_solicitud'),
]