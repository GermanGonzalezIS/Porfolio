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
                         'anterior':'mandamientos_judiciales:lista',
                         'app':'mandamientos_judiciales:verificar_curp',
                         'feria_binacional':True,
                         'feria_app':'a mandamientos judiciales'}
        return render(request,'tramites/pedir_curp.html',extra_context)

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    if validar_curp(curp):
        # Se verifica si hay un trámite pendiente con la curp indicada
        mandamientos_judiciales = MandamientosJudiciales.objects.filter(curp=curp).last()
        
        if mandamientos_judiciales == None:
            # No existe ningún trámite con la curp indicada. Se crea uno nuevo
            return nuevo_tramite(request,curp)
        else:
            # Ya existe algún trámite con la curp indicada
            tramite = get_object_or_404(Tramite,id=mandamientos_judiciales.tramite_id)
            if tramite.estado_id == 1:
                # Se continúa con el trámite encontrado para registrar sus documentos faltantes
                return HttpResponseRedirect('/mandamientos-judiciales/completar/' + str(mandamientos_judiciales.id))
            else:
                # Ya se había solicitado con anterioridad un mandamiento judicial
                # Se crea una nueva solicitud
                return nuevo_tramite(request,curp)
    else:
        messages.error(request,'Por favor introduzca una CURP válida')
        return redirect('mandamientos_judiciales:pedir_curp')

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
    mandamientos_judiciales = MandamientosJudiciales()
    mandamientos_judiciales.curp = curp
    mandamientos_judiciales.tramite_id = tramite.id
    mandamientos_judiciales.save()
    mandamientos_judiciales = MandamientosJudiciales.objects.get(id=mandamientos_judiciales.id)
    return HttpResponseRedirect('/mandamientos-judiciales/completar/' + str(mandamientos_judiciales.id))


class ListaMandamientosJudiciales(ListView,PermissionRequiredMixin):
    permission_required = 'mandamientos_judiciales.view_mandamientosjudiciales'
    model = MandamientosJudiciales
    context_object_name = 'mandamientos_judiciales'
    extra_context = {'app':'mandamientos_judiciales:lista',
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
            lista_mandamientos_judiciales= MandamientosJudiciales.objects.filter(tramite__empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['mandamientos_judiciales'] = lista_mandamientos_judiciales
            return self.render_to_response(context)

class NuevaMandamientosJudiciales(CreateView,PermissionRequiredMixin):
    permission_required = 'mandamientos_judiciales.add_mandamientosjudiciales'
    model = MandamientosJudiciales
    form_class = MandamientosJudicialesForm
    extra_context = {'editar': False}
    success_url = reverse_lazy('mandamientos_judiciales:lista')

class DetalleMandamientosJudiciales(DetailView,PermissionRequiredMixin):
    permission_required = 'mandamientos_judiciales.view_mandamientosjudiciales'
    model = MandamientosJudiciales
    context_object_name = 'mandamientos_judiciales'
    extra_context = {'app':'mandamientos_judiciales:lista'}

class EditarMandamientosJudiciales(UpdateView,PermissionRequiredMixin):
    permission_required = 'mandamientos_judiciales.change_mandamientosjudiciales'
    model = MandamientosJudiciales
    form_class = MandamientosJudicialesForm
    form_beneficiario = BeneficiarioForm
    extra_context = {
        'boton':'Guardar',
        'form_beneficiario':form_beneficiario,
        'template_tramite':'mandamientos_judiciales/mandamientosjudiciales_form.html',
        'feria_binacional': True
    }

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        mandamientos_judiciales = self.object
        context = self.get_context_data()
        curp = mandamientos_judiciales.curp 

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
        context['app'] = 'mandamientos_judiciales:lista'
        return self.render_to_response(context)

    
    def post(self,request,*args,**kwargs):
        lista_documentos = ['acta_nac_original','curp_act','comprobante_domicilio',
        'pasaporte_vigente','matricula_consular','pago_en_caja_fiscalia','fotografia','ine_familiar'] 
        if all(documento in request.POST for documento in lista_documentos):
            # Todos los documentos del trámite fueron seleccionados.
            # Se guardan, y se continúa en la misma página para capturar
            # los datos del beneficiario
            return super().post(request,*args,**kwargs)
        else:
            # Faltaron documentos por seleccionar
            messages.success(self.request,'¡Registro guardado exitosamente!')
            super().post(request,*args,**kwargs)
            return redirect('mandamientos_judiciales:lista')
       
    def get_success_url(self):
        return self.request.path

class EliminarMandamientosJudiciales(DeleteView,PermissionRequiredMixin):
    permission_required = 'mandamientos_judiciales.delete_mandamientosjudiciales'
    model = MandamientosJudiciales

    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de mandamientos judiciales
        tramite_id = kwargs['pk']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        tramite.delete()
        messages.success(self.request,'¡Registro eliminado exitosamente!')
        return redirect('mandamientos_judiciales:lista')      