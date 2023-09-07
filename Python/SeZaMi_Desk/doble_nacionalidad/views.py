from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .forms import *
from .models import * 
from empleados.models import Empleado
from beneficiarios.models import *
from beneficiarios.forms import *
from catalogos.forms import *

class ListaDobleNacionalidad(ListView,PermissionRequiredMixin):
    permission_required = 'defensoria_publica.view_defensoria_publica'
    model = DobleNacionalidad
    context_object_name = 'doble_nacionalidad'
    extra_context = {'app':'doble_nacionalidad:lista',
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
            lista_defensoria_publica = DobleNacionalidad.objects.filter(tramite__empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['defensoria_publica'] = lista_defensoria_publica
            return self.render_to_response(context)

class NuevaDobleNacionalidad(CreateView): # Esta clase se utiliza para crear nuevos registros de doble nacionalidad
    model = DobleNacionalidad
    form_class = DobleNacionalidadForm
    extra_context = {'etiqueta':'Registrar','boton':'Registrar'}
    success_url = reverse_lazy('doble_nacionalidad:lista') # Nos redirecciona a la lista de personas desaparecidas

    

    def form_valid(self, form):
        self.persona = form.save(commit=False)
        # Se obtiene los datos del empleado que esta realizando el registro
        empleado = get_object_or_404(Empleado,username=self.request.user.username)
        # Se guarda en el registro de la persona desaparecida al empleado que realizo el registro
        self.persona.empleado = empleado
        self.persona.save()
        messages.success(self.request,'¡Registro guardado exitosamente!')
        return super(NuevaDobleNacionalidad, self).form_valid(form)

    def form_invalid(self,form):
        print(form.errors)


