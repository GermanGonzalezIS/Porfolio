from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from gestion_publicaciones.forms import RevisionForm
from publicaciones.forms import PublicacionForm
from publicaciones.models import Publicacion
from gestion_publicaciones.models import Estado, Revision
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages


from usuarios.models import Usuario
from django.http import FileResponse, HttpResponse
from django.core.files import File


# Lista de publicaciones
class MisPublicacionesList(PermissionRequiredMixin, ListView):
    permission_required = 'publicaciones.add_publicacion'
    template_name = "mis_publicaciones_list.html"
    model = Publicacion

    def get_queryset(self):
        usuario_actual = self.request.user
        return Publicacion.objects.filter(autor=usuario_actual.id)

# Página de inicio

# Lista de revisiones pendientes


class RevisionesList(PermissionRequiredMixin, ListView):
    permission_required = 'gestion_publicaciones.change_revision'
    template_name = 'publicaciones_revisar_list.html'
    model = Revision

    def get_queryset(self):
        usuario_actual = self.request.user
        return Revision.objects.filter(usuario_revisor=usuario_actual.id)


class InicioView(TemplateView):
    template_name = "inicio.html"


class RevisionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'gestion_publicaciones.change_revision'
    template_name = 'publicacion_revisar_update.html'
    model = Revision
    form_class = RevisionForm

    def post(self, request, *args, **kwargs):
        form = RevisionForm(request.POST, request.FILES)
        if form.is_valid():
            revision_id = self.kwargs['pk']
            revision_actual = Revision.objects.get(id=revision_id)
            revision_actual.estado = Estado.objects.get(
                id=request.POST['estado'])
            # Si hay algún archivo seleccionado
            if(len(request.FILES) != 0):
                revision_actual.archivo = request.FILES['archivo']
            revision_actual.save()
            messages.success(
                request, 'Tu revisión se ha guardado con éxito')
            return redirect('/revisar-publicaciones/')
        else:
            print("----------- Falló")
            return redirect('/revisar-publicaciones/')


# Nueva publicación
class PublicacionNueva(PermissionRequiredMixin, CreateView):
    permission_required = 'publicaciones.add_publicacion'
    template_name = "publicacion_create.html"
    model = Publicacion
    form_class = PublicacionForm
    success_url = reverse_lazy('publicaciones:mis-publicaciones')

    def post(self, request, *args, **kwargs):
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_publicacion = Publicacion(archivo=request.FILES['archivo'])
            nueva_publicacion.titulo = request.POST['titulo']
            nueva_publicacion.autor = Usuario.objects.filter(
                id=request.user.id).first()
            nueva_publicacion.save()
            messages.success(
                request, 'Tu publicación se ha cargado con éxito y pronto será revisada')
            return redirect('/mis-publicaciones/')
        else:
            return redirect('/mis-publicaciones/')


def handler403(request, *args, **argv):
    response = render('403.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 403
    return response


def descargar_publicacion(request, id):
    publicacion = Publicacion.objects.get(id=id)
    filename = publicacion.archivo.path

    # Para descarga directa
    archivo = open(filename, 'rb')
    myfile = File(archivo)
    response = HttpResponse(myfile, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + \
        publicacion.archivo.name
    return response


# por el momento no se implementará, se mantendrá en caso de que el stakeholder quiera
# manejar PDF's posteriormente.
def visualizar_publicacion(request, id):
    publicacion = Publicacion.objects.get(id=id)
    filename = publicacion.archivo.path
    response = FileResponse(open(filename, 'rb'))
    return response
