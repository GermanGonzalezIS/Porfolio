from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import resolve
from django.contrib import messages

from .models import AtencionMigrantes
from beneficiarios.models import Beneficiario, BeneficiarioDireccion, EstudioSocioeconomico
from beneficiarios.forms import BeneficiarioForm, BeneficiarioDireccionForm, EstudioSocioeconomicoForm
from tramites.models import Tramite, EstadoTramite
from empleados.models import Empleado
from .forms import AtencionMigrantesForm
from tramites.forms import PedirCurpForm
from tramites.models import Tramite
from catalogos.forms import *
from tramites.validators import validar_curp


class AtencionMigrantesPrincipal(PermissionRequiredMixin, ListView):
    permission_required = 'atencion_migrantes.view_atencionmigrantes'
    model = AtencionMigrantes
    template_name = "atencion_migrantes_principal.html"
    extra_context = {'app' : 'atencion_migrantes:principal', 
                     'color' : '#cacde0'}

class AtencionMigrantesDetalle(PermissionRequiredMixin,DetailView):
    permission_required = 'atencion_migrantes.view_atencionmigrantes'
    model = AtencionMigrantes
    extra_context = {'app':'atencion_migrantes:principal'}

class AtencionMigrantesEliminar(PermissionRequiredMixin, DeleteView):
    permission_required = 'atencion_migrantes.delete_atencionmigrantes'
    model = AtencionMigrantes

    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de atencion_migrantes
        tramite_id = kwargs['pk']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        tramite.delete()
        messages.success(self.request,'¡Registro eliminado exitosamente!')
        return redirect('atencion_migrantes:principal')

class AtencionMigrantesNuevo(PermissionRequiredMixin,CreateView):
    permission_required = 'atencion_migrantes.add_atencionmigrantes'
    model = AtencionMigrantes
    form_class = AtencionMigrantesForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    template_name = "atencion_migrantes/atencionmigrantes_form.html"
    form_beneficiario = BeneficiarioForm
    extra_context = {
        'etiqueta':'Nuevo', 
        'boton':'Agregar', 
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
        'form_beneficiario':form_beneficiario,
    }
    success_url = reverse_lazy('atencion_migrantes:principal')

class AtencionMigrantesActualizar(UpdateView, PermissionRequiredMixin):
    permission_required = 'atencion_migrantes.change_atencionmigrantes'
    model = AtencionMigrantes
    form_class = AtencionMigrantesForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    form_beneficiario = BeneficiarioForm
    form_municipio = MunicipioForm
    form_localidad = LocalidadForm
    form_asentamiento = AsentamientoForm
    template_name = "atencion_migrantes/atencionmigrantes_form.html"
    extra_context = {
        'etiqueta':'Actualizar', 
        'boton':'Guardar',
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
        'form_beneficiario':form_beneficiario,
        'form_municipio':form_municipio,
        'form_localidad':form_localidad,
        'form_asentamiento':form_asentamiento,
    }

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        atencion_migrantes = self.object
        context = self.get_context_data()
        curp = atencion_migrantes.curp 

        beneficiario = Beneficiario.objects.filter(curp=curp).first()
        if beneficiario != None:
            # Los datos del beneficiario ya habían sido capturados, por lo tanto, se llenan
            # los campos del formulario automáticamente
            direccion = BeneficiarioDireccion.objects.filter(id=beneficiario.direccion_id).first()
            estudio = EstudioSocioeconomico.objects.filter(id=beneficiario.estudio_socioeconomico_id).first()
            form_beneficiario = BeneficiarioForm(instance=beneficiario)
            form_direccion = BeneficiarioDireccionForm(instance=direccion)
            form_estudio = EstudioSocioeconomicoForm(instance=estudio)
            context['form_beneficiario'] = form_beneficiario
            context['form_direccion'] = form_direccion
            context['form_estudio'] = form_estudio
            context['url_beneficiario'] = 'beneficiarios:editar' 
            context['id_beneficiario'] = curp 
        else:
            context['url_beneficiario'] = 'beneficiarios:crear' 
        context['app'] = 'atencion_migrantes:principal'
        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):
        lista_documentos = ['identificacion_oficial','curp_doc','rfc','solicitud_gobernador','hoja_deportacion',
        'comprobante_domicilio','acta_nacimiento']
        
        if all(documento in request.POST for documento in lista_documentos):
            # Todos los documentos del trámite fueron seleccionados.
            # Se guardan, y se continúa en la misma página para capturar
            # los datos del beneficiario
            return super().post(request,*args,**kwargs)
        else:
            # Faltaron documentos por seleccionar
            messages.success(self.request,'¡Registro guardado exitosamente!')
            super().post(request,*args,**kwargs)
            return redirect('atencion_migrantes:principal')
        
    def get_success_url(self):
        return self.request.path

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    curp = curp.upper()
    # Se valida la curp
    if validar_curp(curp):
        # Se verficia si hay algún trámite ya registrado con esa curp
        tramites_registrados = AtencionMigrantes.objects.filter(curp=curp)
        cant_tramites = tramites_registrados.count() # ...
        
        if cant_tramites == 0:
            # No existe ningún trámite con la CURP indicada, por lo tanto se 
            # crea uno nuevo

            # Creación del proceso trámite
            tramite = Tramite()
            tramite.estado_id = 1
            # Se asigna el tipo de trámite para consultar el nombre
            tramite.tipo_tramite_id = 13
            empleado = get_object_or_404(Empleado,username=request.user.username)
            tramite.empleado_id = empleado.id
            # Se verifica, en base a la CURP, si la información del beneficiario ya ha sido capturada.
            if Beneficiario.objects.filter(curp=curp).first() != None:
                # Los datos del beneficiario ya se encuentran capturados en el sistema
                # Se agrega la curp al proceso del trámite
                tramite.beneficiario_id = curp
                
            tramite.save()
            tramite = Tramite.objects.latest('id')

            # Creación trámite específico
            atencion_migrantes = AtencionMigrantes()
            atencion_migrantes.curp = curp
            atencion_migrantes.tramite_id = tramite.id
            atencion_migrantes.save()
            atencion_migrantes = AtencionMigrantes.objects.latest('id')
            return HttpResponseRedirect('/atencion-migrantes/completar/' + str(atencion_migrantes.id))
        else:
            # Ya existe un trámite con la CURP indicada
            tramite_atencion = tramites_registrados.first()
            tramite_general = Tramite.objects.filter(id=tramite_atencion.tramite_id).first()
            if tramite_general.estado_id == 1:
                id_pendiente = tramites_registrados.latest("id").id
                return HttpResponseRedirect('/atencion-migrantes/completar/' + str(id_pendiente))
            else:
                # El trámite con la CURP indicada ya entregó toda la documentación necesaria y fueron
                # capturados los datos del beneficiario, por lo tanto el flujo de la aplicación reedirige
                # al usuario a la lista de trámites de 'Apoyo a Migrantes...'
                messages.error(request,'Ya existe un trámite asociado a esta CURP')
                return redirect('atencion_migrantes:pedir_curp')
    else:
        messages.error(request,'Por favor introduzca una CURP válida')
        return redirect('atencion_migrantes:pedir_curp')

def pedir_curp(request):
    if request.method == "GET":
        form = PedirCurpForm()
        extra_context = {'form':form,
                         'anterior':'atencion_migrantes:principal',
                         'app':'atencion_migrantes:verificar_curp'}
        return render(request,'tramites/pedir_curp.html',extra_context)
