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
from datetime import date

def pedir_curp(request):
    if request.method == "GET":
        form = PedirCurpForm()
        extra_context = {'form':form,
                         'anterior':'defensoria_publica:lista',
                         'app':'defensoria_publica:verificar_curp',
                         'feria_binacional':True,
                         'feria_app':'a defensoría pública'}
        return render(request,'tramites/pedir_curp.html',extra_context)

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    if validar_curp(curp):
        # Se verifica si hay un trámite pendiente con la curp indicada
        defensoria_publica = DefensoriaPublica.objects.filter(curp=curp).last()
        
        if defensoria_publica == None:
            # No existe ningún trámite con la curp indicada. Se crea uno nuevo
            return nuevo_tramite(request,curp)
        else:
            # Ya existe algún trámite con la curp indicada
            tramite = get_object_or_404(Tramite,id=defensoria_publica.tramite_id)
            if tramite.estado_id == 1:
                # Se continúa con el trámite encontrado para registrar sus documentos faltantes
                return HttpResponseRedirect('/defensoria-publica/completar/' + str(defensoria_publica.id))
            else:
                # Ya se había solicitado con anterioridad una constancia de estudio. 
                # Se crea una nueva solicitud
                return nuevo_tramite(request,curp)
    else:
        messages.error(request,'Por favor introduzca una CURP válida')
        return redirect('defensoria_publica:pedir_curp')

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
    defensoria_publica = DefensoriaPublica()
    defensoria_publica.curp = curp
    defensoria_publica.tramite_id = tramite.id
    defensoria_publica.save()
    defensoria_publica = DefensoriaPublica.objects.get(id=defensoria_publica.id)
    return HttpResponseRedirect('/defensoria-publica/completar/' + str(defensoria_publica.id))

class ListaDefensoriaPublica(ListView,PermissionRequiredMixin):
    permission_required = 'defensoria_publica.view_defensoriapublica'
    model = DefensoriaPublica
    context_object_name = 'defensoria_publica'
    extra_context = {'app':'defensoria_publica:lista',
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
            lista_defensoria_publica = DefensoriaPublica.objects.filter(tramite__empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['defensoria_publica'] = lista_defensoria_publica
            return self.render_to_response(context)

class NuevaDefensoriaPublica(CreateView,PermissionRequiredMixin):
    permission_required = 'defensoria_publica.add_defensoriapublica'
    model = DefensoriaPublica
    form_class = DefensoriaPublicaForm
    extra_context = {'editar': False}
    success_url = reverse_lazy('defensoria_publica:lista')

class DetalleDefensoriaPublica(DetailView,PermissionRequiredMixin):
    permission_required = 'defensoria_publica.view_defensoriapublica'
    model = DefensoriaPublica
    context_object_name = 'defensoria_publica'
    extra_context = {'app':'defensoria_publica:lista'}

class EliminarDefensoriaPublica(DeleteView,PermissionRequiredMixin):
    permission_required = 'defensoria_publica.delete_defensoriapublica'
    model = DefensoriaPublica

    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de constancia estudios
        tramite_id = kwargs['pk']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        tramite.delete()
        messages.success(self.request,'¡Registro eliminado exitosamente!')
        return redirect('defensoria_publica:lista')

class EditarDefensoriaPublica(UpdateView,PermissionRequiredMixin):
    permission_required = 'defensoria_publica.change_defensoriapublica'
    model = DefensoriaPublica
    form_class = DefensoriaPublicaForm
    form_beneficiario = BeneficiarioForm
    extra_context = {
        'boton':'Guardar',
        'form_beneficiario':form_beneficiario,
        'template_tramite':'defensoria_publica/defensoriapublica_form.html',
        'feria_binacional': True
    }

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        defensoria_publica = self.object
        context = self.get_context_data()
        curp = defensoria_publica.curp 

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
        context['app'] = 'defensoria_publica:lista'
        return self.render_to_response(context)

    
    def post(self,request,*args,**kwargs):
        campos_obligatorios = ['tramite_realizar','num_telefonico','email']
        datos = request.POST
        for campo in datos:
            if (campo in campos_obligatorios) and (datos[campo] == ''):
                # Alguno de los campos obligatorios no tienen ningún dato capturado, por tanto,
                # no se puede proceder a llenar los datos del beneficiario.
                # Los datos son válidos, pero faltaron documentos por entregar
                messages.success(self.request,'¡Registro guardado exitosamente!')
                super().post(request,*args,**kwargs)
                return redirect('constancia_estudios:lista')
        # Los datos son válidos, pero faltaron documentos por entregar
        return super().post(request,*args,**kwargs)

    def get_success_url(self):
        return self.request.path