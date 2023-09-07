from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

from .models import *
from catalogos.models import *
from tramites.models import Tramite
from .forms import BeneficiarioForm, BeneficiarioDireccionForm, EstudioSocioeconomicoForm
from apostillas.models import Apostilla
from apostillas.forms import ApostillaForm


class BeneficiariosPrincipal(PermissionRequiredMixin, ListView):
    permission_required = 'beneficiarios.view_beneficiario'
    model = Beneficiario
    template_name = "beneficiarios_principal.html"

class BeneficiariosDetalle(PermissionRequiredMixin, DetailView):
    permission_required = 'beneficiarios.view_beneficiario'
    model = Beneficiario
    
    def get_context_data(self, **kwargs):
        curp_beneficiario = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['tramites_list'] = Tramite.objects.filter(beneficiario_id=curp_beneficiario)
        return context
    
class BeneficiariosEditar(UpdateView, PermissionRequiredMixin):
    permission_required = 'beneficiarios.change_beneficiario'
    model = Beneficiario
    form_class = BeneficiarioForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm

    extra_context = {
        'etiqueta':'Actualizar datos del',
        'boton':'Guardar',
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
    }

    #success_url = reverse_lazy('beneficiarios:principal')


    def get(self, request,*args, **kwargs):
        self.object = self.get_object()
        beneficiario = self.object
        context = self.get_context_data()
        curp = beneficiario.curp
        print('\n\n' + 'HOLA MUNDOOOO' + '\n\n')

        # Obtener datos del beneficiario
        direccion = BeneficiarioDireccion.objects.filter(id=beneficiario.direccion_id).first()
        estudio = EstudioSocioeconomico.objects.filter(id=beneficiario.estudio_socioeconomico_id).first()
        form_direccion = BeneficiarioDireccionForm(instance=direccion)
        form_estudio = EstudioSocioeconomicoForm(instance=estudio)
        context['form_direccion'] = form_direccion
        context['form_estudio'] = form_estudio
        context['id_beneficiario'] = curp
        return self.render_to_response(context)



    def post(self,request,*args,**kwargs):
        beneficiario = get_object_or_404(Beneficiario,curp=request.POST['curp'])
        direccion = get_object_or_404(BeneficiarioDireccion,id=beneficiario.direccion_id)
        estudio = get_object_or_404(EstudioSocioeconomico,id=beneficiario.estudio_socioeconomico_id)
        # Se crean los formularios tomando como base el registro existente en la base de datos
        # y capturando los cambios hechos a través del template
        form_beneficiario = BeneficiarioForm(request.POST,instance=beneficiario)
        form_direccion = BeneficiarioDireccionForm(request.POST,instance=direccion)
        form_estudio = EstudioSocioeconomicoForm(request.POST,instance=estudio)

        if form_beneficiario.is_valid() and form_direccion.is_valid() and form_estudio.is_valid():
            estudio = form_estudio.save()
            direccion = form_direccion.save()
            beneficiario = form_beneficiario.save()
            # Se asignan los datos sobre la dirección y estudiosocioeconomico 
            # al beneficiario en cuestion
            beneficiario.direccion_id = direccion.id
            beneficiario.estudio_socioeconomico_id = estudio.id
            beneficiario.save()

            # Se verifica si la ejecución de la vista viene desde un trámite
            if 'app' in request.POST:
                # Se obtiene el trámite para relizar su asociación al beneficiario
                tramite_id = request.POST['tramite_id']
                tramite = get_object_or_404(Tramite,id=tramite_id)
                # Se asocia la CURP del beneficiario al tramite solicitado.
                tramite.beneficiario_id = beneficiario.curp
                # En caso de estar todos los datos correctos, se cambia el estado del trámite
                tramite.estado_id = 2
                tramite.save()
                messages.success(self.request,'¡Registro guardado exitosamente!')
                return redirect(request.POST['app'])
            else:
                messages.success(self.request,'¡Registro guardado exitosamente!')
                return redirect('beneficiarios:principal')
        else:
            extra_context = {}
            extra_context['form'] = get_tramite_form(request.POST['template_tramite'],request.POST['tramite_id'])
            extra_context['form_beneficiario'] = form_beneficiario
            extra_context['form_direccion'] = form_direccion
            extra_context['form_estudio'] = form_estudio
            extra_context['url_beneficiario'] = 'beneficiarios:editar'
            extra_context['id_beneficiario'] = request.POST['curp']  
            extra_context['app'] = request.POST['app']  
            extra_context['template_tramite'] = request.POST['template_tramite']
            extra_context['boton'] = 'Guardar'
            messages.error(request,'El formulario contiene datos inválidos')
            return render(request,request.POST['template_tramite'],extra_context)

class BeneficiariosCrear(CreateView, PermissionRequiredMixin):
    permission_required = 'beneficiarios.add_beneficiario'
    model = Beneficiario
    form_class = BeneficiarioForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    extra_context = {
        'etiqueta':'Registrar nuevo',
        'boton':'Guardar',
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
    }
    success_url = reverse_lazy('beneficiarios:principal')

    def post(self,request,*args,**kwargs):
        tramite_id = request.POST['tramite_id']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        form_beneficiario = BeneficiarioForm(request.POST)
        form_direccion = BeneficiarioDireccionForm(request.POST)
        form_estudio = EstudioSocioeconomicoForm(request.POST)

        if form_beneficiario.is_valid() and form_direccion.is_valid() and form_estudio.is_valid():
            estudio = form_estudio.save()
            direccion = form_direccion.save()
            beneficiario = form_beneficiario.save()
            beneficiario.direccion_id = direccion.id
            beneficiario.estudio_socioeconomico_id = estudio.id
            beneficiario.save()
            # Se asocia la CURP del beneficiario al tramite solicitado.
            tramite.beneficiario_id = beneficiario.curp
            # En caso de estar todos los datos correctos, se cambia el estado del trámite
            tramite.estado_id = 2
            tramite.save()
            return redirect(request.POST['app'])
        else:
            extra_context = {}
            extra_context['form'] = get_tramite_form(request.POST['template_tramite'],request.POST['tramite_id'])
            extra_context['form_beneficiario'] = form_beneficiario
            extra_context['form_direccion'] = form_direccion
            extra_context['form_estudio'] = form_estudio
            extra_context['url_beneficiario'] = 'beneficiarios:crear'
            extra_context['app'] = request.POST['app']  
            extra_context['template_tramite'] = request.POST['template_tramite']
            extra_context['boton'] = 'Guardar'
            messages.error(request,'El formulario contiene datos inválidos')
            return render(request,request.POST['template_tramite'],extra_context)

class BeneficiariosEliminar(PermissionRequiredMixin, DeleteView):
    permission_required = 'beneficiarios.delete_beneficiario'
    model = Beneficiario
    success_url = reverse_lazy('beneficiarios:principal')

def nueva_direccion(request):
    if request.method == "POST":
        form = BeneficiarioDireccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria:lista')

def nuevo_estudio(request):
    if request.method == "POST":
        form = BeneficiarioDireccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria:lista')

def get_tramite_form(template_tramite,tramite_id):
    if template_tramite == "apostillas/apostilla_form.html":
        apostilla = get_object_or_404(Apostilla,tramite_id=tramite_id)    
        return ApostillaForm(instance=apostilla)

# =============================Especial para ferias=================
class BeneficiariosCrearFerias(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    extra_context = {
        'etiqueta':'Registrar nuevo',
        'boton':'Guardar',
    }
    success_url = reverse_lazy('beneficiarios:principal')

    def post(self,request,*args,**kwargs):
        tramite_id = request.POST['tramite_id']
        tramite = get_object_or_404(Tramite,id=tramite_id)
        form_beneficiario = BeneficiarioForm(request.POST)

        if form_beneficiario.is_valid():
            beneficiario = form_beneficiario.save()
            beneficiario.save()
            # Se asocia la CURP del beneficiario al tramite solicitado.
            tramite.beneficiario_id = beneficiario.curp
            # En caso de estar todos los datos correctos, se cambia el estado del trámite
            tramite.estado_id = 2
            print("Hola, si cambié XDDDDDD")
            tramite.save()
            return redirect(request.POST['app'])
        else:
            extra_context = {}
            extra_context['form'] = get_tramite_form(request.POST['template_tramite'],request.POST['tramite_id'])
            extra_context['form_beneficiario'] = form_beneficiario
            extra_context['url_beneficiario'] = 'beneficiarios:crear_feria'
            extra_context['app'] = request.POST['app']  
            extra_context['template_tramite'] = request.POST['template_tramite']
            extra_context['boton'] = 'Guardar'
            messages.error(request,'El formulario contiene datos inválidos')
            return render(request,request.POST['template_tramite'],extra_context)

class BeneficiariosEditarFerias(UpdateView):
    model = Beneficiario
    form_class = BeneficiarioForm

    extra_context = {
        'etiqueta':'Actualizar datos del',
        'boton':'Guardar',
    }

    #success_url = reverse_lazy('beneficiarios:principal')


    def get(self, request,*args, **kwargs):
        self.object = self.get_object()
        beneficiario = self.object
        context = self.get_context_data()
        curp = beneficiario.curp
        print('\n\n' + 'HOLA MUNDOOOO' + '\n\n')

        # Obtener datos del beneficiario
        context['id_beneficiario'] = curp
        return self.render_to_response(context)



    def post(self,request,*args,**kwargs):
        beneficiario = get_object_or_404(Beneficiario,curp=request.POST['curp'])
        # Se crean los formularios tomando como base el registro existente en la base de datos
        # y capturando los cambios hechos a través del template
        form_beneficiario = BeneficiarioForm(request.POST,instance=beneficiario)

        if form_beneficiario.is_valid():
            beneficiario = form_beneficiario.save()
            # Se asignan los datos sobre la dirección y estudiosocioeconomico 
            # al beneficiario en cuestion
            beneficiario.save()

            # Se verifica si la ejecución de la vista viene desde un trámite
            if 'app' in request.POST:
                # Se obtiene el trámite para relizar su asociación al beneficiario
                tramite_id = request.POST['tramite_id']
                tramite = get_object_or_404(Tramite,id=tramite_id)
                # Se asocia la CURP del beneficiario al tramite solicitado.
                tramite.beneficiario_id = beneficiario.curp
                # En caso de estar todos los datos correctos, se cambia el estado del trámite
                tramite.estado_id = 2
                tramite.save()
                messages.success(self.request,'¡Registro guardado exitosamente!')
                return redirect(request.POST['app'])
            else:
                messages.success(self.request,'¡Registro guardado exitosamente!')
                return redirect('beneficiarios:principal')
        else:
            extra_context = {}
            extra_context['form'] = get_tramite_form(request.POST['template_tramite'],request.POST['tramite_id'])
            extra_context['form_beneficiario'] = form_beneficiario
            extra_context['url_beneficiario'] = 'beneficiarios:editar_feria'
            extra_context['id_beneficiario'] = request.POST['curp']  
            extra_context['app'] = request.POST['app']  
            extra_context['template_tramite'] = request.POST['template_tramite']
            extra_context['boton'] = 'Guardar'
            messages.error(request,'El formulario contiene datos inválidos')
            return render(request,request.POST['template_tramite'],extra_context)