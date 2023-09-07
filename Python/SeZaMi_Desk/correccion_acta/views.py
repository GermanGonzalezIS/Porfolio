from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .forms import *
from .models import * 
from tramites.models import Tramite
from tramites.forms import PedirCurpForm
from empleados.models import Empleado
from beneficiarios.models import *
from beneficiarios.forms import *
from catalogos.forms import *
from tramites.validators import validar_curp

def pedir_curp(request):
    if request.method == "GET":
        form = PedirCurpForm()
        extra_context = {'form':form,
                         'anterior':'correccion_acta:lista',
                         'app':'correccion_acta:verificar_curp',
                         'feria_binacional':True,
                         'feria_app':'a corrección de acta'}
        return render(request,'tramites/pedir_curp.html',extra_context)

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    if validar_curp(curp):
        # Se verifica si hay un trámite pendiente con la curp indicada
        correccion_acta = CorreccionActa.objects.filter(curp=curp).last()
        
        if correccion_acta == None:
            # No existe ningún trámite con la curp indicada. Se crea uno nuevo
            return nuevo_tramite(request,curp)
        else:
            # Ya existe algún trámite con la curp indicada
            tramite = get_object_or_404(Tramite,id=correccion_acta.tramite_id)
            if tramite.estado_id == 1:
                # Se continúa con el trámite encontrado para registrar sus documentos faltantes
                return HttpResponseRedirect('/correcion-acta/completar/' + str(correccion_acta.id))
            else:
                # Ya se había solicitado con anterioridad un mandamiento judicial
                # Se crea una nueva solicitud
                return nuevo_tramite(request,curp)
    else:
        messages.error(request,'Por favor introduzca una CURP válida')
        return redirect('correccion_acta:pedir_curp')

def nuevo_tramite(request,curp):
    # Creación del proceso trámite
    tramite = Tramite()
    tramite.estado_id = 1
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
    correccion_acta = CorreccionActa()
    correccion_acta.curp = curp
    correccion_acta.tramite_id = tramite.id
    correccion_acta.save()
    correccion_acta = CorreccionActa.objects.get(id=correccion_acta.id)
    return HttpResponseRedirect('/correccion-acta/completar/' + str(correccion_acta.id))

class ListaCorreccionActa(ListView,PermissionRequiredMixin):
    permission_required = 'correccion_acta.view_correccionacta'
    model = CorreccionActa
    context_object_name = 'correccion_acta'
    extra_context = {'app':'correccion_acta:lista',
                     'color':'#b4ddc9'}
    
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
            lista_correccion_acta= CorreccionActa.objects.filter(tramite__empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['correccion_acta'] = lista_correccion_acta
            return self.render_to_response(context)

class NuevaCorreccionActa(CreateView,PermissionRequiredMixin):
    permission_required = 'correccion_acta.add_correccionacta'
    model = CorreccionActa
    form_class = CorreccionActaForm
    extra_context = {'editar': False}
    success_url = reverse_lazy('correccion_acta:lista')

class DetalleCorreccionActa(DetailView,PermissionRequiredMixin):
    permission_required = 'correccion_acta.view_correccionacta'
    model = CorreccionActa
    context_object_name = 'correccion_acta'
    extra_context = {'app':'correccion_acta:lista'}

class EliminarCorreccionActa(DeleteView,PermissionRequiredMixin):
    permission_required = 'correccion_acta.delete_correccionacta'
    model = CorreccionActa

    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de mandamientos judiciales
        tramite_id = kwargs['pk']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        tramite.delete()
        messages.success(self.request,'¡Registro eliminado exitosamente!')
        return redirect('correccion_acta:lista')      

class EditarCorreccionActa(UpdateView,PermissionRequiredMixin):
    permission_required = 'correccion_acta.change_correccionacta'
    model = CorreccionActa
    form_class = CorreccionActaForm
    form_beneficiario = BeneficiarioForm
    extra_context = {
        'boton':'Guardar',
        'form_beneficiario':form_beneficiario,
        'template_tramite':'correccion_acta/correccionacta_form.html',
        'feria_binacional': True
    }

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        correccion_acta = self.object
        context = self.get_context_data()
        curp = correccion_acta.curp 

        beneficiario = Beneficiario.objects.filter(curp=curp).first()

        if beneficiario != None:
            # Los datos del beneficiario ya habían sido capturados, por lo tanto, se llenan
            # los campos del formulario automáticamente
            form_beneficiario = BeneficiarioForm(instance=beneficiario)
            context['form_beneficiario'] = form_beneficiario
            context['url_beneficiario'] = 'beneficiarios:editar_feria' 
            context['id_beneficiario'] = curp 
        else:
            context['url_beneficiario'] = 'beneficiarios:crear_feria'
        # Indica la sección del sistema a la que se desea regresar una vez guardado el trámite
        context['app'] = 'correccion_acta:lista'
        return self.render_to_response(context)

    
    def post(self,request,*args,**kwargs):
        lista_documentos = ['acta_a_corregir','documentos_comprobantes','testimonial',
        'solicitud_firmado','original_copias'] 
        if all(documento in request.POST for documento in lista_documentos):
            # Todos los documentos del trámite fueron seleccionados.
            # Se guardan, y se continúa en la misma página para capturar
            # los datos del beneficiario
            return super().post(request,*args,**kwargs)
        else:
            # Faltaron documentos por seleccionar
            messages.success(self.request,'¡Registro guardado exitosamente!')
            super().post(request,*args,**kwargs)
            return redirect('correccion_acta:lista')
       
    def get_success_url(self):
        return self.request.path
