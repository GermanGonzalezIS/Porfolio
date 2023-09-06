from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.core.mail import EmailMessage
from gestion_publicaciones.models import Estado, Revision
from publicaciones.models import Publicacion
from usuarios.models import Usuario
from django.views.generic import TemplateView
from .token import token_estado


# Create your views here.
class PublicacionesList(ListView):

    model = Publicacion
    template_name = 'publicaciones_list.html'


def detalle_publicacion(request, pk):

    publicacion_seleccionada = get_object_or_404(Publicacion, id=pk)
    revisiones = Revision.objects.filter(publicacion=publicacion_seleccionada)
    if revisiones.count() != 0:

        revisiones_ralizadas = 0
        for revision in revisiones:

            if revision.archivo:

                revisiones_ralizadas = revisiones_ralizadas + 1
        context = {'publicacion': publicacion_seleccionada,
                   'revisiones': revisiones,
                   'estatus': revisiones_ralizadas}
    else:

        context = {'publicacion': publicacion_seleccionada}
    return render(request, 'publicacion_detail.html', context)


def mostrar_lista_revisores(request, pk):

    publicacion_seleccionada = get_object_or_404(Publicacion, id=pk)
    usuarios = Usuario.objects.filter().all()
    revisores = []
    for usuario in usuarios:

        if es_revisor(usuario):

            revisores.append(usuario)
    context = {'publicacion': publicacion_seleccionada,
               'revisores': revisores}
    return render(request, 'revisores_list.html', context)


def es_revisor(user):

    return user.groups.filter(name='Revisor').exists()


def asignar_revisores(request):

    publicacion_seleccionada = get_object_or_404(Publicacion,
                                                 id=int(request.POST['publicacion']))
    if request.method == 'POST':

        contador = 0
        for item in request.POST:

            if request.POST[item] == 'Selected' and contador < 4:

                revisor = Usuario.objects.get(id=int(item))
                revision = Revision.objects.create(publicacion=publicacion_seleccionada,
                                                   usuario_revisor=revisor,
                                                   estado=Estado.objects.get(descripcion='En espera'))
                revision.save()
                contador = contador + 1
                enviar_correo(revision,
                              revisor,
                              publicacion_seleccionada,
                              request)

    return redirect('gestion_publicaciones:detalle_publicacion',
                    pk=publicacion_seleccionada.id)


def enviar_correo(revision, usuario, publicacion, request):

    dominio = get_current_site(request)
    rid = urlsafe_base64_encode(force_bytes(revision.id))
    token = token_estado.make_token(revision)
    if revision.estado == Estado.objects.get(descripcion='En espera'):

        mensaje = render_to_string('solicitud_revision.html',
                                   {
                                       'usuario': usuario,
                                       'dominio': dominio,
                                       'publicacion': publicacion,
                                       'rid': rid,
                                       'revision': revision,
                                       'token': token,
                                       'aceptar': 'Aceptada',
                                       'rechazar': 'Rechazada'
                                   })
        asunto = 'Solicitud de revisión'

    else:

        mensaje = render_to_string('recordatorio_revision.html',
                                   {
                                       'usuario': usuario,
                                       'dominio': dominio,
                                       'publicacion': publicacion
                                   })
        asunto = 'Recordatorio de revisión'

    to = usuario.correo_electronico
    email = EmailMessage(
        asunto,
        mensaje,
        to=[to]
    )
    email.content_subtype = 'html'
    email.send()


class CambiarEstadoSolicitud(TemplateView):

    def get(self, request, *args, **kwargs):

        try:

            rid = urlsafe_base64_decode(kwargs['rid64'])
            estado = kwargs['estado']
            token = kwargs['token']
            revision = Revision.objects.get(id=rid)
        except:

            revision = None
        if revision and token_estado.check_token(revision, token):

            if estado == 'Aceptada':

                revision.estado = Estado.objects.get(descripcion='Aceptada')
                messages.success(self.request,
                                 'Aceptaste la solicitud de revisión')
            else:

                revision.estado = Estado.objects.get(descripcion='Rechazada')
                messages.error(self.request,
                               'Rechazaste la solicitud de revisión')
            revision.save()
        else:
            messages.success(self.request,
                             'Aceptaste la solicitud de revisión')
            messages.error(self.request,
                           'No se realizó la acción correctamente')
        return redirect('usuarios:login')


def recordatorio(request, pk):

    revision = get_object_or_404(Revision, id=pk)
    publicacion = Publicacion.objects.get(id=revision.publicacion.id)
    usuario = Usuario.objects.get(id=revision.usuario_revisor.id)
    enviar_correo(revision, usuario, publicacion, request)
    messages.success(request,
                     'Se envió recordatorio al usuario '+str(usuario))
    return redirect('gestion_publicaciones:detalle_publicacion',
                    pk=publicacion.id)


def cambiar_revisor(request, pk):

    if request.method == 'GET':
        revision = get_object_or_404(Revision, id=pk)
        revisiones = Revision.objects.all().filter(publicacion=revision.publicacion)
        usuarios_disponibles = []
        usuarios_no_disponibles = []
        usuarios = Usuario.objects.all()
        for r in revisiones:

            usuarios_no_disponibles.append(r.usuario_revisor.id)
        for usuario in usuarios:

            if es_revisor(usuario) and usuario.id not in usuarios_no_disponibles:

                usuarios_disponibles.append(usuario)
        context = {'revision': revision,
                   'usuarios_disponibles': usuarios_disponibles,
                   'publicacion': revision.publicacion}
        return render(request, 'asignar_nuevo_revisor.html', context)
    else:

        revision = get_object_or_404(Revision, id=pk)
        usuario = Usuario.objects.get(id=int(request.POST['usuario']))
        revision.usuario_revisor = usuario
        revision.estado = Estado.objects.get(descripcion='En espera')
        revision.save()
        enviar_correo(revision, usuario, revision.publicacion, request)
        return redirect('gestion_publicaciones:detalle_publicacion',
                        pk=revision.publicacion.id)
