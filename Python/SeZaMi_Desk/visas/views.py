from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from empleados.models import Empleado
from .models import Visa
from .forms import VisaForm
from tramites.models import Tramite
from tramites.forms import PedirCurpForm
from empleados.models import Empleado
from beneficiarios.models import *
from beneficiarios.forms import *
from catalogos.forms import *
from tramites.validators import validar_curp

class ListaVisa(PermissionRequiredMixin,ListView):
    permission_required = 'visas.view_visa'
    model = Visa
    context_object_name = 'visas'

    def get(self,request,*args,**kwargs):
        user = request.user
        if user.is_superuser == 1:
            return super().get(request,*args,**kwargs)
        # Se obtiene el usuario logueado
        usuario = get_object_or_404(Empleado,username=request.user.username)
        # Se obtiene el grupo al que pertenece el usuario (Super Admin, Admin o Capturista)
        grupo_usuario = usuario.grupo_id
        if grupo_usuario == 3 or grupo_usuario == 2:
            # Es Super Admin o admin  
            return super().get(request,*args,**kwargs)  
        else:
            # Es capturista, se muestran solamente los trámites que el usuario ha realizado
            lista_visas = Visa.objects.filter(empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['visas'] = lista_visas
            return self.render_to_response(context)

class NuevaVisa(CreateView,PermissionRequiredMixin):
    permission_required = 'visas.add_visa'
    model = Visa
    form_class = VisaForm
    success_url = reverse_lazy('visas:lista')
    
    def form_valid(self, form):
        self.visa = form.save(commit=False)
        # Se obtiene los datos del empleado que esta realizando el registro
        empleado = get_object_or_404(Empleado,username=self.request.user.username)
        # Se guarda en el registro de la Visa al empleado que realizo el registro
        self.visa.empleado = empleado
        self.visa.save()
        messages.success(self.request,'¡Registro guardado exitosamente!')
        return super(NuevaVisa, self).form_valid(form)
   
class DetalleVisa(PermissionRequiredMixin,DetailView):
    permission_required = 'visas.view_visa'
    model = Visa
    context_object_name = 'visa'

class EditarVisa(PermissionRequiredMixin,UpdateView,SuccessMessageMixin):
    permission_required = 'visas.change_visa'
    model = Visa
    form_class = VisaForm
    success_url = reverse_lazy('visas:lista')
    
    def form_valid(self,form):
        messages.success(self.request,'¡Registro actualizado exitosamente!')
        return super(EditarVisa, self).form_valid(form)

class EliminarVisa(PermissionRequiredMixin,DeleteView):
    permission_required = 'visas.delete_visa'
    model = Visa
    success_url = reverse_lazy('visas:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '¡Registro eliminado exitosamente!')
        return super(EliminarVisa, self).delete(request, *args, **kwargs)