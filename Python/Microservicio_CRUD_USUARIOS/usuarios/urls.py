#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: urls.py
#
# Descripción:
#   
#-------------------------------------------------------------------------

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UsuariosPublicoViewSet, UsuariosAutenticadoViewSet

urlpatterns = [
    path('nuevo', UsuariosPublicoViewSet.as_view({
        'post': 'create'
    })),
    path('login', UsuariosPublicoViewSet.as_view({
        'post': 'login'
    })),
    path('logout', UsuariosAutenticadoViewSet.as_view({
        'post': 'logout'
    })),
    path('perfil', UsuariosAutenticadoViewSet.as_view({
        'get': 'detalles_perfil'
    })),
    path('modificar-perfil', UsuariosAutenticadoViewSet.as_view({
        'post': 'modificar_perfil'
    })),
    path('eliminar-perfil', UsuariosAutenticadoViewSet.as_view({
        'get': 'eliminar_perfil'
    })),
    path('lista-usuarios', UsuariosAutenticadoViewSet.as_view({
        'get': 'lista_usuarios'
    })),
    path('lista-administradores', UsuariosAutenticadoViewSet.as_view({
        'get': 'lista_administradores'
    })),
    path('detalle-usuario/<str:user>', UsuariosAutenticadoViewSet.as_view({
        'get': 'detalle_usuario'
    })),
    path('eliminar-usuario/<str:user>', UsuariosAutenticadoViewSet.as_view({
        'get': 'eliminar_usuario'
    })),
    path('detalle-permisos/<str:user>', UsuariosAutenticadoViewSet.as_view({
        'get': 'detalle_permisos'
    })),
    path('modificar-permisos/<str:user>', UsuariosAutenticadoViewSet.as_view({
        'post': 'modificar_permisos'
    })),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
