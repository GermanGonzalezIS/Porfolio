from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Apostilla
from tramites.models import Tramite
from .forms import ApostillaForm
from tramites.forms import PedirCurpForm
from empleados.models import Empleado
from beneficiarios.models import *
from beneficiarios.forms import *
from catalogos.forms import *
from tramites.validators import validar_curp

class ListaApostilla(PermissionRequiredMixin,ListView):
    permission_required = 'apostillas.view_apostilla'
    model = Apostilla    
    context_object_name = 'apostillas'
    extra_context = {'app':'apostillas:lista',
                     'color':'#c9ccdf'}

    def get(self,request,*args,**kwargs):
        # Se obtiene el usuario logueado
        usuario = get_object_or_404(Empleado,username=request.user.username)
        # Se obtiene el grupo al que pertenece el usuario (Super Admin, Admin o Capturista)
        grupo_usuario = usuario.grupo_id
        if grupo_usuario == 3 or grupo_usuario == 2:
            # Es Super Admin o admin  
            return super().get(request,*args,**kwargs)  
        else:
            # Es capturista, se muestran solamente los trámites que el usuario ha realizado
            lista_apostillas = Apostilla.objects.filter(tramite__empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['apostillas'] = lista_apostillas
            return self.render_to_response(context)

class NuevaApostilla(PermissionRequiredMixin,CreateView):
    permission_required = 'apostillas.add_apostilla'
    model = Apostilla
    form_class = ApostillaForm
    extra_context = {'editar': False}
    success_url = reverse_lazy('apostillas:lista')

class DetalleApostilla(PermissionRequiredMixin,DetailView):
    permission_required = 'apostillas.view_apostilla'
    model = Apostilla
    context_object_name = 'apostilla'
    extra_context = {'app':'apostillas:lista'}

class EditarApostilla(UpdateView,PermissionRequiredMixin,SuccessMessageMixin):
    permission_required = 'apostillas.change_apostilla'
    model = Apostilla
    form_class = ApostillaForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    form_beneficiario = BeneficiarioForm
    template_name = "apostillas/apostilla_form.html"
    extra_context = {
        'boton':'Guardar',
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
        'form_beneficiario':form_beneficiario,
        'template_tramite':'apostillas/apostilla_form.html',
    }

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        apostilla = self.object
        context = self.get_context_data()
        curp = apostilla.curp 

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
        # Indica la sección del sistema a la que se desea regresar una vez guardado el trámite
        context['app'] = 'apostillas:lista'
        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):
        lista_documentos = ['acta_americana','acta_mexicana','identificacion_padres',
        'curp_doc','comprobante_domicilio','rfc']
        
        if all(documento in request.POST for documento in lista_documentos):
            # Todos los documentos del trámite fueron seleccionados.
            # Se guardan, y se continúa en la misma página para capturar
            # los datos del beneficiario
            return super().post(request,*args,**kwargs)
        else:
            # Faltaron documentos por seleccionar
            messages.success(self.request,'¡Registro guardado exitosamente!')
            super().post(request,*args,**kwargs)
            return redirect('apostillas:lista')
        
    def get_success_url(self):
        return self.request.path

class EliminarApostilla(PermissionRequiredMixin,DeleteView):
    permission_required = 'apostillas.delete_apostilla'
    model = Apostilla

    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de apostilla
        tramite_id = kwargs['pk']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        tramite.delete()
        messages.success(self.request,'¡Registro eliminado exitosamente!')
        return redirect('apostillas:lista')

def pedir_curp(request):
    if request.method == "GET":
        form = PedirCurpForm()
        extra_context = {'form':form,
                         'anterior':'apostillas:lista',
                         'app':'apostillas:verificar_curp'}
        return render(request,'tramites/pedir_curp.html',extra_context)

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    if validar_curp(curp):
        # Se verifica si hay un trámite pendiente con la curp indicada
        apostilla = Apostilla.objects.filter(curp=curp).last()
        
        if apostilla == None:
            # No existe ningún trámite con la curp indicada. Se crea uno nuevo
            return nuevo_tramite(request,curp)
        else:
            # Ya existe algún trámite con la curp indicada
            tramite = get_object_or_404(Tramite,id=apostilla.tramite_id)
            if tramite.estado_id == 1:
                # Se continúa con el trámite encontrado para registrar sus documentos faltantes
                return HttpResponseRedirect('/apostillas/completar/' + str(apostilla.id))
            else:
                # Ya se había solicitado con anterioridad una Apostilla. 
                # Se crea una nueva solicitud
                return nuevo_tramite(request,curp)
    else:
        messages.error(request,'Por favor introduzca una CURP válida')
        return redirect('apostillas:pedir_curp')

def nuevo_tramite(request,curp):
    # Creación del proceso trámite
    tramite = Tramite()
    tramite.estado_id = 1
    tramite.tipo_tramite_id = 1
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
    apostilla = Apostilla()
    apostilla.curp = curp
    apostilla.tramite_id = tramite.id
    apostilla.save()
    apostilla = Apostilla.objects.get(id=apostilla.id)
    return HttpResponseRedirect('/apostillas/completar/' + str(apostilla.id))