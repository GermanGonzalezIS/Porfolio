from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.urls import resolve
from django.contrib import messages
from django.urls import reverse

from visas.models import Visa
from .models import CorazonPlata, GrupoVisa
from beneficiarios.models import Beneficiario, BeneficiarioDireccion, EstudioSocioeconomico
from beneficiarios.forms import BeneficiarioForm, BeneficiarioDireccionForm, EstudioSocioeconomicoForm
from tramites.models import Tramite, EstadoTramite, Grupo, Club, Representante
from empleados.models import Empleado
from .forms import CorazonPlataForm, GrupoVisaForm
from tramites.forms import PedirCurpForm
from tramites.models import Tramite
from catalogos.forms import *
from tramites.validators import validar_curp


# NOTA: Este trámite debe permitir más de un trámite por persona
class GrupoVisaList(ListView):
    model = GrupoVisa
    template_name = "corazon_plata/grupovisa_list.html"
    extra_context = {'app' : 'corazon_plata:lista', 
                     'color' : '#FFFFFF'}

class GrupoVisaNuevo(CreateView):
    model = GrupoVisa
    form_class = GrupoVisaForm
    template_name = "corazon_plata/grupovisa_form.html"
    extra_context = {
        'etiqueta':'Nuevo', 
        'boton':'Agregar'
    }
    success_url = reverse_lazy('corazon_plata:lista')

class GrupoVisaActualizar(UpdateView):
    model = GrupoVisa
    form_class = GrupoVisaForm
    template_name = "corazon_plata/grupovisa_form.html"
    extra_context = {
        'etiqueta':'Actualizar', 
        'boton':'Guardar'
    }
    success_url = reverse_lazy('corazon_plata:lista')


class GrupoVisaDetalle(DetailView):
    model = GrupoVisa

    def get_context_data(self, **kwargs):
        id_grupo_visa = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context["corazonplata_list"] = CorazonPlata.objects.filter(grupo_visa = id_grupo_visa) 
        return context
    

class GrupoVisaEliminar(DeleteView):
    model = GrupoVisa
    success_url = reverse_lazy('corazon_plata:lista')

class CorazonPlataList(ListView):
    model = CorazonPlata
    extra_context = {'app' : 'corazon_plata:lista', 
                     'color' : '#FFFFFF'}

    
class CorazonPlataDetalle(DetailView):
    model = CorazonPlata

class CorazonPlataEliminar(DeleteView):
    model = CorazonPlata

    def get_success_url(self):
        self.object = self.get_object()
        corazon_plata = self.object
        return reverse('corazon_plata:detalle_grupo', kwargs={'pk': corazon_plata.grupo_visa.id})



class CorazonPlataNuevo(CreateView):
    model = CorazonPlata
    form_class = CorazonPlataForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    template_name = "corazon_plata/corazonplata_form.html"
    form_beneficiario = BeneficiarioForm


    extra_context = {
        'etiqueta':'Nuevo', 
        'boton':'Agregar', 
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
        'form_beneficiario':form_beneficiario,
    }


    success_url = reverse_lazy('corazon_plata:lista')

    def post(self, request, *args,**kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if 'tipo_post' in request.POST:
            print("\n\n\n" + request.POST.get('grupo_id') + "\n\n\n")
            context['grupo_id'] = request.POST['grupo_id']
            return render(request, 'corazon_plata/corazonplata_form.html', context)
        else:
            return super().post(request,*args,**kwargs)




class CorazonPlataActualizar(UpdateView):
    model = CorazonPlata
    form_class = CorazonPlataForm
    template_name = "corazon_plata/corazonplata_form.html"
    extra_context = {
        'etiqueta':'Actualizar', 
        'boton':'Guardar',
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        corazon_plata = self.object
        context = self.get_context_data()
        context['app'] = 'corazon_plata:lista'
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        corazon_plata = self.object
        lista_documentos = ['credencial', 'pasaporte', 'curp', 'persona_zacatecana', 
        'certificado_medico', 'padrino', 'no_antecedentes', 'nombre_ahijado', 'ap_paterno_ahijado', 'ap_materno_ahijado', 'nombre_padrino']
        print("\n\n\n" + str(request.POST) + "\n\n\n")

        if all(documento in request.POST for documento in lista_documentos):
            # Todos los documentos del trámite fueron seleccionados.
            # Enviar datos para posteriormente llenar los campos de visa
            super().post(request,*args,**kwargs)
            # Obtener registro de corazón de plata correcto
            corazon_plata = CorazonPlata.objects.get(id = corazon_plata.id)
            corazon_plata.datos_completos = True # Marcar como completado
            corazon_plata.save()
            # Se crea un nuevo tramite de visa
            visa_nueva = Visa()
            # Se asigna el grupo de corazón de plata al que pertenece
            visa_nueva.corazon_plata_id = corazon_plata.id
            # Se asignan los nombres capturados en corazón de plata al trámite de visa
            visa_nueva.nombre_solicitante = corazon_plata.nombre_ahijado
            visa_nueva.apellido_paterno_solicitante = corazon_plata.ap_paterno_ahijado
            visa_nueva.apellido_materno_solicitante = corazon_plata.ap_materno_ahijado
            # Se obtiene los datos del empleado que esta realizando el registro
            empleado = get_object_or_404(Empleado,username=self.request.user.username)
            # Se guarda en el registro de la Visa al empleado que realizo el registro
            visa_nueva.empleado = empleado
            #Se extrae el folio del trámite de visa
            folio_visa = visa_nueva.folio
            visa_nueva.save()
            return redirect('/visas/editar/' + str(folio_visa))
        else:
            # Faltaron documentos por seleccionar
            super().post(request,*args,**kwargs)
            return redirect('corazon_plata:lista')
        
    def get_success_url(self):
        return self.request.path


def nuevo_tramite(request):
    # Creación del trámite específico
    corazon_plata = CorazonPlata()
    corazon_plata.grupo_visa_id = request.POST['grupo_id'] 
    corazon_plata.save()
    corazon_plata = CorazonPlata.objects.get(id=corazon_plata.id)

    return HttpResponseRedirect('/corazon-plata/completar/' + str(corazon_plata.id))




