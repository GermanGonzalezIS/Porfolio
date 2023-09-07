from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

from .models import Tramite
from beneficiarios.models import Beneficiario
from .forms import PedirCurpForm, EditarForm, EditarPasaporteSeguroForm
from beneficiarios.forms import BeneficiarioForm
from empleados.models import Empleado

class TramiteList(ListView):
    model = Tramite
    template_name= 'tramites/tramite_list.html'

    def get(self,request,*args,**kwargs):
        lista_tramites = None
        # Se obtiene el usuario logueado
        usuario = get_object_or_404(Empleado,username=request.user.username)
        # Se obtiene el grupo al que pertenece el usuario (Super Admin, Admin o Capturista)
        grupo_usuario = usuario.grupo_id
        if grupo_usuario == 3:
            # Es Super Admin
            return super().get(request,*args,**kwargs)  
        elif grupo_usuario == 2:
            # Es Admin
            return super().get(request,*args,**kwargs)  
        else:
            # Es capturista, se muestran solamente los trámites que el usuario ha realizado
            lista_tramites = Tramite.objects.filter(empleado_id=usuario.id)
        # Se obtiene asigna el context_object_name definido 
        self.object_list = self.get_queryset()
        # Se agregan los trámites filtrados a la lista de variables a pasar al template
        context = self.get_context_data()
        context['object_list'] = lista_tramites
        return self.render_to_response(context)

class TramiteEditar(UpdateView):
    model = Tramite
    form_class = EditarForm
    success_url = reverse_lazy('tramites:lista_tramite') 

class TramiteEditarPasaporteSeguro(UpdateView):
    model = Tramite
    form_class = EditarPasaporteSeguroForm

class TramiteEliminar(DeleteView):
    model = Tramite
    success_url = reverse_lazy('tramites:lista_tramite')

# Función que redirige al template actualizar trámite con su formulario correspondiente.
def actualizar_tramite(request,pk):
    # Se extrae la aplicación de origen del trámite y se aplica un split.
    app = request.POST['app'].split(":")
    # Se extrae el trámite correspondiente.
    tramite = get_object_or_404(Tramite,id=pk)
    # Si la aplicación de origen es pasaportes o seguros el formulario es diferente.
    if (app[0] == 'pasaportes' or app[0] == 'seguros' ):
        form = EditarPasaporteSeguroForm(instance=tramite)
    else:
        form = EditarForm(instance=tramite)
    # Se crea el diccionario del contexto con las variables que necesitará el template.
    context={'form': form ,
             'app' : request.POST['app'] ,
             'tramite' : tramite,
             'color' : request.POST['color']}
    # Redirige al template tramites/tramite_form.html.
    return render(request, 'tramites/tramite_form.html', context)

# Función que guarda los cambios realizados al trámite.
def guardar_acualizacion(request,pk):
    # Se extrae la aplicación de origen del trámite y se aplica un split.
    app = request.POST['app'].split(":")
    # Se extrae el trámite correspondiente.
    tramite = get_object_or_404(Tramite,id=pk)
    # Si la aplicación de origen es pasaportes o seguros el formulario es diferente.
    if (app[0] == 'pasaportes' or app[0] == 'seguros' ):
        # Se extrae el formulario del POST.
        form = EditarPasaporteSeguroForm(request.POST, instance=tramite)
    else:
        # Se extrae el formulario del POST.
        form = EditarForm(request.POST, instance=tramite)
    # Se verifica si el formulario es válido.
    if form.is_valid():
        # Se guarda el formulario.
        messages.success(request,'¡Registro actualizado exitosamente!')
        form.save()
    # Redirecciona a la aplicación de origen.
    return redirect(request.POST['app'])

def pedir_curp(request):
    if request.method == "GET":
        form = PedirCurpForm()
        extra_context = {'form':form}
        return render(request,'tramites/pedir_curp.html',extra_context)
    elif request.method == "POST":
        curp = request.POST['curp']
        cant_beneficiarios = Beneficiario.objects.filter(curp=curp).count()
        beneficiario = Beneficiario()
        if cant_beneficiarios == 0:
            beneficiario.curp = curp
            form = BeneficiarioForm(instance=beneficiario)
            return render(request,'beneficiarios/beneficiario_form.html',{'beneficiario':beneficiario,
                                                                          'form':form,
                                                                          'curp':curp,
                                                                          'etiqueta':'Registrar nuevo',
                                                                          'boton':'Guardar'})
        else:
            beneficiario = Beneficiario.objects.get(curp=curp)
            form = BeneficiarioForm(instance=beneficiario) 
            return render(request,'beneficiarios/beneficiario_form.html',{'beneficiario':beneficiario,
                                                                          'form':form,
                                                                          'curp':curp,
                                                                          'etiqueta':'Registrar nuevo',
                                                                          'boton':'Guardar'})

def ferias_binacionales(request):
    user = get_object_or_404(Empleado, username=request.user.username)
    if user.has_perm('licencia_conducir.view_licenciaconducir') or user.has_perm('constancia_estudio.view_constanciaestudios') or user.has_perm('defensoria_publica.view_defensoriapublica') :
        return render(request,'menu_opciones.html')
    else:
        return render(request,'403.html')
