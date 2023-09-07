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
                         'anterior':'constancia_estudios:lista',
                         'app':'constancia_estudios:verificar_curp',
                         'feria_binacional':True,
                         'feria_app':'a constancia de estudios'}
        return render(request,'tramites/pedir_curp.html',extra_context)

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    if validar_curp(curp):
        # Se verifica si hay un trámite pendiente con la curp indicada
        constancia_estudio = ConstanciaEstudios.objects.filter(curp=curp).last()
        
        if constancia_estudio == None:
            # No existe ningún trámite con la curp indicada. Se crea uno nuevo
            return nuevo_tramite(request,curp)
        else:
            # Ya existe algún trámite con la curp indicada
            tramite = get_object_or_404(Tramite,id=constancia_estudio.tramite_id)
            if tramite.estado_id == 1:
                # Se continúa con el trámite encontrado para registrar sus documentos faltantes
                return HttpResponseRedirect('/constancia-estudios/completar/' + str(constancia_estudio.id))
            else:
                # Ya se había solicitado con anterioridad una constancia de estudio. 
                # Se crea una nueva solicitud
                return nuevo_tramite(request,curp)
    else:
        messages.error(request,'Por favor introduzca una CURP válida')
        return redirect('constancia_estudios:pedir_curp')

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
    constancia_estudio = ConstanciaEstudios()
    constancia_estudio.curp = curp
    constancia_estudio.tramite_id = tramite.id
    constancia_estudio.save()
    constancia_estudio = ConstanciaEstudios.objects.get(id=constancia_estudio.id)
    return HttpResponseRedirect('/constancia-estudios/completar/' + str(constancia_estudio.id))

class ConstanciaEstudioList(ListView,PermissionRequiredMixin):
    permission_required = 'constancia_estudio.view_constanciaestudios'
    model = ConstanciaEstudios
    context_object_name = 'constancia_estudios'
    extra_context = {'app':'constancia_estudios:lista',
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
            lista_constancia_estudios = ConstanciaEstudios.objects.filter(tramite__empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['constancia_estudios'] = lista_constancia_estudios
            return self.render_to_response(context)

class NuevaConstanciaEstudio(CreateView,PermissionRequiredMixin):
    permission_required = 'constancia_estudio.add_constanciaestudios'
    model = ConstanciaEstudios
    form_class = ConstanciaEstudioForm
    extra_context = {'editar': False}
    success_url = reverse_lazy('constancia_estudios:lista')

class DetalleConstanciaEstudio(DetailView,PermissionRequiredMixin):
    permission_required = 'constancia_estudio.view_constanciaestudios'
    model = ConstanciaEstudios
    context_object_name = 'constancia_estudios'
    extra_context = {'app':'constancia_estudios:lista'}

class EditarConstanciaEstudio(UpdateView,PermissionRequiredMixin):
    permission_required = 'constancia_estudio.change_constanciaestudios'
    model = ConstanciaEstudios
    form_class = ConstanciaEstudioForm
    form_beneficiario = BeneficiarioForm
    extra_context = {
        'boton':'Guardar',
        'form_beneficiario':form_beneficiario,
        'template_tramite':'constancia_estudio/constanciaestudios_form.html',
        'feria_binacional': True
    }

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        constancia_estudio = self.object
        context = self.get_context_data()
        curp = constancia_estudio.curp 

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
        context['app'] = 'constancia_estudios:lista'
        return self.render_to_response(context)

    
    def post(self,request,*args,**kwargs):
        if self.validar_campos_llenos(request.POST):
            # Todos los documentos del trámite a entregarse en físico fueron seleccionados,
            # así como también fueron llenados todos los campos obligatorios
            return super().post(request,*args,**kwargs)
        else:
            # Los datos son válidos, pero faltaron documentos por entregar
            messages.success(self.request,'¡Registro guardado exitosamente!')
            super().post(request,*args,**kwargs)
            return redirect('constancia_estudios:lista')

    def validar_campos_llenos(self,datos):
        lista_documentos = ['fotografia']
        campos_obligatorios = ['nombre_escuela','anio_aprox','num_telefonico','email']
        if all(documento in datos for documento in lista_documentos):
            # Se entregaron los documentos requeridos en físico
            for campo in datos:
                if (campo in campos_obligatorios) and (datos[campo] == ''):
                    # Alguno de los campos obligatorios no tienen ningún dato capturado, por tanto,
                    # no se puede proceder a llenar los datos del beneficiario.
                    return False
        else:
            # No se entregó alguno o ambos documetos solicitados en físico.
            return False
        # Se entregaron todos los documentos requeridos en físico y se llenaron los campos
        # obligatorios del trámite
        return True
        
    def get_success_url(self):
        return self.request.path

class EliminarConstanciaEstudio(DeleteView,PermissionRequiredMixin):
    permission_required = 'constacia_estudio.delete_constanciaestudio'
    model = ConstanciaEstudios

    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de constancia estudios
        tramite_id = kwargs['pk']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        tramite.delete()
        messages.success(self.request,'¡Registro eliminado exitosamente!')
        return redirect('constancia_estudios:lista')

