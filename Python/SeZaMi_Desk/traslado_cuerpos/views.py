from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from empleados.models import Empleado
from .models import TrasladoCuerpo
from .forms import TrasladoCuerpoForm

class ListaTrasladoCuerpo(PermissionRequiredMixin,ListView):
    permission_required = 'trasladocuerpo.view_trasladocuerpo'
    model = TrasladoCuerpo
    context_object_name = 'traslados'

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
            lista_traslados = TrasladoCuerpo.objects.filter(empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['traslados'] = lista_traslados
            return self.render_to_response(context)

class EditarTrasladoCuerpo(PermissionRequiredMixin,UpdateView):
    permission_required = 'trasladocuerpo.change_trasladocuerpo'
    model = TrasladoCuerpo
    form_class = TrasladoCuerpoForm
    success_url = reverse_lazy('traslado_cuerpos:lista')

    def form_valid(self,form):
        messages.success(self.request,'¡Registro actualizado exitosamente!')
        return super(EditarTrasladoCuerpo, self).form_valid(form)

class AgregarTrasladoCuerpo(PermissionRequiredMixin,CreateView):
    permission_required = 'trasladocuerpo.add_trasladocuerpo'
    model = TrasladoCuerpo
    form_class = TrasladoCuerpoForm
    success_url = reverse_lazy('traslado_cuerpos:lista')

    def form_invalid(self,form):
        print("**************************")
        print(form.errors)

    def form_valid(self, form):
        self.traslado = form.save(commit=False)
        # Se obtiene los datos del empleado que esta realizando el registro
        empleado = get_object_or_404(Empleado,username=self.request.user.username)
        # Se guarda en el registro de la Visa al empleado que realizo el registro
        self.traslado.empleado = empleado
        self.traslado.save()
        messages.success(self.request,'¡Registro guardado exitosamente!')
        return super(AgregarTrasladoCuerpo, self).form_valid(form)
        
class EliminarTrasladoCuerpo(PermissionRequiredMixin,DeleteView):
    permission_required = 'trasladocuerpo.delete_trasladocuerpo'
    model = TrasladoCuerpo
    success_url = reverse_lazy('traslado_cuerpos:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '¡Registro eliminado exitosamente!')
        return super(EliminarTrasladoCuerpo, self).delete(request, *args, **kwargs)

class DetalleTrasladoCuerpo(PermissionRequiredMixin,DetailView):
    permission_required = 'trasladocuerpo.view_trasladocuerpo'
    model = TrasladoCuerpo
    context_object_name = 'traslado'
