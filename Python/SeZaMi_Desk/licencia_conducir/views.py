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
                         'anterior':'licencia_conducir:lista',
                         'app':'licencia_conducir:verificar_curp',
                         'feria_binacional':True,
                         'feria_app':'a licencia de conducir'}
        return render(request,'tramites/pedir_curp.html',extra_context)

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    if validar_curp(curp):
        # Se verifica si hay un trámite pendiente con la curp indicada
        licencia_conducir = LicenciaConducir.objects.filter(curp=curp).last()
        
        if licencia_conducir == None:
            # No existe ningún trámite con la curp indicada. Se crea uno nuevo
            return nuevo_tramite(request,curp)
        else:
            # Ya existe algún trámite con la curp indicada
            tramite = get_object_or_404(Tramite,id=licencia_conducir.tramite_id)
            if tramite.estado_id == 1:
                # Se continúa con el trámite encontrado para registrar sus documentos faltantes
                return HttpResponseRedirect('/licencia-conducir/completar/' + str(licencia_conducir.id))
            else:
                # Ya se había solicitado con anterioridad una licencia de conducir.
                # Se crea una nueva solicitud
                return nuevo_tramite(request,curp)
    else:
        messages.error(request,'Por favor introduzca una CURP válida')
        return redirect('licencia_conducir:pedir_curp')

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
    licencia_conducir = LicenciaConducir()
    licencia_conducir.curp = curp
    licencia_conducir.tramite_id = tramite.id
    licencia_conducir.save()
    licencia_conducir = LicenciaConducir.objects.get(id=licencia_conducir.id)
    return HttpResponseRedirect('/licencia-conducir/completar/' + str(licencia_conducir.id))


class ListaLicenciaConducir(ListView,PermissionRequiredMixin):
    permission_required = 'licencia_conducir.view_licenciaconducir'
    model = LicenciaConducir
    context_object_name = 'licencia_conducir'
    extra_context = {'app':'licencia_conducir:lista',
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
            lista_licencia_conducir= LicenciaConducir.objects.filter(tramite__empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['licencia_conducir'] = lista_licencia_conducir
            return self.render_to_response(context)

class NuevaLicenciaConducir(CreateView,PermissionRequiredMixin):
    permission_required = 'licencia_conducir.add_licenciaconducir'
    model = LicenciaConducir
    form_class = LicenciaConducirForm
    extra_context = {'editar': False}
    success_url = reverse_lazy('licencia_conducir:lista')

class DetalleLicenciaConducir(DetailView,PermissionRequiredMixin):
    permission_required = 'licencia_conducir.view_licenciaconducir'
    model = LicenciaConducir
    context_object_name = 'licencia_conducir'
    extra_context = {'app':'licencia_conducir:lista'}

class EditarLicenciaConducir(UpdateView,PermissionRequiredMixin):
    permission_required = 'licencia_conducir.change_licenciaconducir'
    model = LicenciaConducir
    form_class = LicenciaConducirForm
    form_beneficiario = BeneficiarioForm
    extra_context = {
        'boton':'Guardar',
        'form_beneficiario':form_beneficiario,
        'template_tramite':'licencia_conducir/licenciaconducir_form.html',
        'feria_binacional': True
    }

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        licencia_conducir= self.object
        context = self.get_context_data()
        curp = licencia_conducir.curp 

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
        context['app'] = 'licencia_conducir:lista'
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
            return redirect('licencia_conducir:lista')

    def validar_campos_llenos(self,datos):
        lista_documentos = ['acta_nacimiento','comprobante_dom_eeuu','referencia_dom_zac','fotografia','identificacion_oficial']
        campos_obligatorios = ['tipo_sangre']
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

class EliminarLicenciaConducir(DeleteView,PermissionRequiredMixin):
    permission_required = 'licencia_conducir.delete_licenciaconducir'
    model = LicenciaConducir

    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de constancia estudios
        tramite_id = kwargs['pk']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        tramite.delete()
        messages.success(self.request,'¡Registro eliminado exitosamente!')
        return redirect('licencia_conducir:lista')        
