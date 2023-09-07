from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import sys
import redis
from .tokens import get_token_for_user

from .models import Usuario, Entidad_Federativa
from .serializers import UsuarioSerializer

from .models import Usuario

def crear_SuperAdmin(names,f_lastname,s_lastname,curp,email,entidad):

    nuevo_usuario = Usuario.objects.create(
        first_name = names,
        last_name = f_lastname,
        segundo_apellido = s_lastname,
        username = "SUPER-ADMIN",
        curp = curp,
        email = email,
        fecha_nacimiento = "2000-07-16",
        entidad = Entidad_Federativa.objects.get(clave=entidad),
        super_admin=True
    )
    
    nuevo_usuario.set_password("Sup3r4dm1n1026$$$")
    nuevo_usuario.save()

    return True

redis_app = redis.Redis(host="172.15.0.2", port=6379)



# Clase que contiene los métodos públicos del microservicio de Usuarios
class UsuariosPublicoViewSet(viewsets.ViewSet):
    permission_classes = []

    # Método que añade un usuario
    def create(self, request):
        # Se busca el nombre de usuario dado en la base de datos
        usuario_existe = Usuario.objects.filter(username=request.data['username']).exists()
        # Se busca la CURP dada en la base de datos
        curp_existe = Usuario.objects.filter(curp=request.data['curp']).exists()
        # Se busca la entidad dada en la base de datos
        entidad_existe = Entidad_Federativa.objects.filter(clave=request.data['entidad']).exists()

        # Si el nombre de usuario y la curp no se encuentran en la base de datos y si la entidad
        # si se encuentra en la base de datos continua con la creación del nuevo usuario
        if usuario_existe != True and curp_existe != True and entidad_existe == True:

            # Se llenan los datos del usuario con los campos del formulario
            nuevo_usuario = Usuario.objects.create(
                first_name = request.data['first_name'],
                last_name = request.data['last_name'],
                segundo_apellido = request.data['segundo_apellido'],
                username = request.data['username'],
                curp = request.data['curp'],
                email = request.data['correo'],
                fecha_nacimiento = request.data['fecha_nacimiento'],
                entidad = Entidad_Federativa.objects.get(clave=request.data['entidad'])
            )
            # Se añade la contraseña dada
            nuevo_usuario.set_password(request.data['password'])
            # Se guarda el usuario
            nuevo_usuario.save()
            # Se serializan los datos del usuario
            serializer = UsuarioSerializer(nuevo_usuario)
            
            # Si el usuario se encuentra autenticado continua la generación de la respuesta
            if nuevo_usuario.is_authenticated == True :

                # Se crea el token
                token = get_token_for_user(nuevo_usuario)
                # Se guarda en redis el usuario logeado
                redis_app.mset({ nuevo_usuario.username : token })
                # Se crea la respuesta
                respuesta = {
                    'usuario' : serializer.data,
                    'token' : token
                }
                # Regresa la respuesta y el estatus 201
                return Response(respuesta, status=status.HTTP_201_CREATED)

            else:

                # Regresa la respuesta y el estatus 401
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:

            # Se crea la respuesta con los errores encontrados
            respuesta = {
                'entidad_existente': str(entidad_existe),
                'usr_existente' : str(usuario_existe),
                'curp_existente' : str(curp_existe)
            }
            # Se regresa la respuesta y el estatus 302
            return Response(data=respuesta, status=status.HTTP_302_FOUND)

    # Función de Login
    def login(self, request):
        # Se extraen los datos de la petición
        username = request.data['username']
        password = request.data['password']
        # Verifica que el usuario exista y que el password sea el correspondiente
        usuario = authenticate(username=username, password=password)

        # Si usuario no es None significa que se encontro el usuario y que el password es el correcto
        if usuario is not None and redis_app.exists(username) == 0:

            usuario_logeado = Usuario.objects.filter(username=username).first()
            # Se serializa los datos del usuario
            serializer = UsuarioSerializer(usuario_logeado)
            # Se crea el token de acceso
            token = get_token_for_user(usuario_logeado)
            # Se guarda vel usuario logeado en redis
            redis_app.mset({ username : token })
            #Se crea la respuesta
            respuesta = {
                    'usuario' : serializer.data,
                    'token' : token
                }
            # Se regresa la respuesta y el estatus 202
            return Response(respuesta, status=status.HTTP_202_ACCEPTED)

        else:

            # Se regresa el estatus 401
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        

# Clase que contieene los métodos donde se necesita estar autenticado para acceder a ellos
class UsuariosAutenticadoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]

    def logout(self, request):
        username = str(request.data["username"])
        token = str(request.data["token"])

        if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

            redis_app.delete(username)
            return  Response(status=status.HTTP_200_OK)
        else:

            return Response  (status=status.HTTP_400_BAD_REQUEST)

    def detalles_perfil(self, request):
        
        if 'Username' in request.headers and 'Token' in request.headers:
            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                usuario = Usuario.objects.filter(username=username).first()
                serializer = UsuarioSerializer(usuario)
                respuesta = {
                    "usuario" : serializer.data,
                    "entidad" : usuario.entidad.clave
                }

                return  Response(respuesta, status=status.HTTP_200_OK)
            else:

                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def modificar_perfil(self, request):
        
        if 'Username' in request.headers and 'Token' in request.headers:
            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                entidad_existe = Entidad_Federativa.objects.filter(clave=request.data['entidad']).exists()

                if entidad_existe == True:
                    usuario = Usuario.objects.filter(username=username).first()
                    usuario.first_name = request.data['first_name']
                    usuario.last_name = request.data['last_name']
                    usuario.segundo_apellido = request.data['segundo_apellido']
                    usuario.email = request.data['email']
                    usuario.fecha_nacimiento = request.data['fecha_nacimiento']
                    usuario.entidad = Entidad_Federativa.objects.get(clave=request.data['entidad'])

                    usuario.save()

                    return  Response(status=status.HTTP_200_OK)
            else:

                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def eliminar_perfil(self, request):

        if 'Username' in request.headers and 'Token' in request.headers:
            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):
                usuario = Usuario.objects.filter(username=username).first()
                redis_app.delete(username)
                usuario.delete()
                return  Response(status=status.HTTP_200_OK)
            else :
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def lista_usuarios(self, request):

        if 'Username' in request.headers and 'Token' in request.headers:

            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                usuario = Usuario.objects.filter(username=username).first()

                if usuario.admin == True or usuario.super_admin == True:

                    usuarios = Usuario.objects.filter(super_admin=False, admin=False)
                    lista_serializer = UsuarioSerializer(usuarios, many=True)
                    usuario_serializer = UsuarioSerializer(usuario)
                    respuesta = {
                        "usuario": usuario_serializer.data,
                        "lista": lista_serializer.data
                    }
                    return  Response(respuesta, status=status.HTTP_200_OK)
                    
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def lista_administradores(self, request):

        if 'Username' in request.headers and 'Token' in request.headers:

            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                usuario = Usuario.objects.filter(username=username).first()

                if usuario.super_admin == True:

                    usuarios = Usuario.objects.filter(super_admin=False, admin=True)
                    lista_serializer = UsuarioSerializer(usuarios, many=True)
                    usuario_serializer = UsuarioSerializer(usuario)
                    respuesta = {
                        "usuario": usuario_serializer.data,
                        "lista": lista_serializer.data
                    }
                    return  Response(respuesta, status=status.HTTP_200_OK)
                    
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def detalle_usuario(self, request, user):

        if 'Username' in request.headers and 'Token' in request.headers:

            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                usuario = Usuario.objects.filter(username=username).first()

                if usuario.admin == True or usuario.super_admin == True:

                    user_detalle = get_object_or_404(Usuario, username=user)
                    user_detalle_serializer = UsuarioSerializer(user_detalle)
                    usuario_serializer = UsuarioSerializer(usuario)
                    entidad = user_detalle.entidad.clave
                    respuesta = {
                        "usuario": usuario_serializer.data,
                        "detalle_usuario": user_detalle_serializer.data,
                        "entidad": entidad
                    }
                    return  Response(respuesta, status=status.HTTP_200_OK)
                    
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def eliminar_usuario(self, request, user):

        if 'Username' in request.headers and 'Token' in request.headers:

            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                usuario = Usuario.objects.filter(username=username).first()

                if usuario.admin == True or usuario.super_admin == True:

                    user_delete = get_object_or_404(Usuario, username=user)
                    if redis_app.exists(user_delete.username) == 1:
                        redis_app.delete(username)
                    user_delete.delete()
                    return  Response(status=status.HTTP_200_OK)
                
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def detalle_permisos(self, request, user):
        
        if 'Username' in request.headers and 'Token' in request.headers:
            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                usuario = Usuario.objects.filter(username=username).first()

                if usuario.admin == True or usuario.super_admin == True:

                    usuario_permiso = get_object_or_404(Usuario, username=user)
                    usuario_serializer = UsuarioSerializer(usuario)
                    usuario_permiso_serializer = UsuarioSerializer(usuario_permiso)
                    respuesta = {
                        "usuario" : usuario_serializer.data,
                        "usuario_permiso" : usuario_permiso_serializer.data
                    }

                    return  Response(respuesta, status=status.HTTP_200_OK)
                else:

                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:

                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def modificar_permisos(self, request, user):

        if 'Username' in request.headers and 'Token' in request.headers:
            username = request.headers['Username']
            token = request.headers['Token']

            if redis_app.exists(username) == 1 and redis_app.get(str(username)).decode("utf-8") == str(token):

                usuario = Usuario.objects.filter(username=username).first()

                if usuario.admin == True or usuario.super_admin == True:

                    usuario_permiso = get_object_or_404(Usuario, username=user)
                    try:
                        usuario_permiso.admin = request.data['admin']
                        usuario_permiso.super_admin = False
                    except:
                        pass
                    
                    try: 
                        usuario_permiso.super_admin = request.data['super_admin']
                        usuario_permiso.admin = False
                    except:
                        pass

                    usuario_permiso.save()
                    return  Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)