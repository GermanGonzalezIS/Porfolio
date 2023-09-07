from django.urls import path
from . import views

app_name = 'empleados'

urlpatterns = [
    path('lista/', views.EmpleadoList.as_view(), name='lista'),
    path('nuevo/', views.NuevoEmpleado.as_view(), name='nuevo'),
    path('detalle/<int:pk>', views.detalleEmpleado, name='detalle'),
    path('permisos/<int:pk>', views.permisos, name='permisos'),
    path('agrega-permisos/<int:pk>', views.agregaPermiso, name='agrega-permisos'),
    path('eliminar/<int:pk>', views.EliminarEmpleado.as_view(), name='eliminar'),
    path('modificar/<int:pk>', views.ModificarEmpleado.as_view(), name='modificar'),
    path('grupo/<int:pk>', views.seleccionaGrupo, name='grupo'),
    path('seleccionar-permisos/', views.seleccionarPermisos, name='seleccionar-permisos'),
    path('login/', views.login, name='login'),
    path('logout/', views.EmpleadoLogout.as_view(), name='logout'),
    path('perfil/', views.verPerfil, name='perfil'),
]