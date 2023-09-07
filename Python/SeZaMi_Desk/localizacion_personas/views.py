from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from empleados.models import Empleado
from .models import PersonaDesaparecida
from .forms import PersonaDesaparecidaForm

class ListaPersonasDesaparecidas(PermissionRequiredMixin,ListView): # Esta clase se utiliza para mostrar la lista de personas desaparecidas
    permission_required = 'localizacion_personas.view_personadesaparecida' # Se especifica el registro necesario para acceder a esta vista
    model = PersonaDesaparecida
    context_object_name = 'personas'

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
            lista_personas = PersonaDesaparecida.objects.filter(empleado_id=usuario.id)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = self.get_queryset()
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            context['personas'] = lista_personas
            return self.render_to_response(context)

class AgregarPersonaDesaparecida(PermissionRequiredMixin,CreateView): # Esta clase se utiliza para crear nuevos registros de personas desaparecidas
    permission_required = 'localizacion_personas.add_personadesaparecida' # Se especifica el registro necesario para acceder a esta vista
    model = PersonaDesaparecida
    form_class = PersonaDesaparecidaForm
    extra_context = {'etiqueta':'Registrar','boton':'Registrar'}
    success_url = reverse_lazy('localizacion_personas:lista') # Nos redirecciona a la lista de personas desaparecidas
    def form_valid(self, form):
        self.persona = form.save(commit=False)
        # Se obtiene los datos del empleado que esta realizando el registro
        empleado = get_object_or_404(Empleado,username=self.request.user.username)
        # Se guarda en el registro de la persona desaparecida al empleado que realizo el registro
        self.persona.empleado = empleado
        self.persona.save()
        messages.success(self.request,'¡Registro guardado exitosamente!')
        return super(AgregarPersonaDesaparecida, self).form_valid(form)

class EditarPersonaDesaparecida(PermissionRequiredMixin,UpdateView): # Esta clase se utiliza para editar los registros de las personas desaparecidas
    permission_required = 'localizacion_personas.change_personadesaparecida' # Se especifica el registro necesario para acceder a esta vista
    model = PersonaDesaparecida
    form_class = PersonaDesaparecidaForm
    extra_context = {'etiqueta':'Editar','boton':'Guardar','grupo_admin':False}
    success_url = reverse_lazy('localizacion_personas:lista')
    def get(self,request,*args,**kwargs):
        user = request.user
        # Se obtiene el usuario logueado
        usuario = get_object_or_404(Empleado,username=request.user.username)
        # Se obtiene el grupo al que pertenece el usuario (Super Admin, Admin o Capturista)
        grupo_usuario = usuario.grupo_id
        if grupo_usuario == 3 or grupo_usuario == 2:
            # Es Super Admin o admin
            self.extra_context['grupo_admin'] = True
        else:
            self.extra_context['grupo_admin'] = False
        return super().get(request,*args,**kwargs)
    def form_valid(self, form):
        messages.success(self.request,'¡Registro actualizado exitosamente!')
        return super(EditarPersonaDesaparecida, self).form_valid(form)


class DetallePersonaDesaparecida(PermissionRequiredMixin,DetailView): # Esta clase se utiliza para mostrar los detalles de los registros de las personas desaparecidas
    permission_required = 'localizacion_personas.view_personadesaparecida' # Se especifica el registro necesario para acceder a esta vista
    model = PersonaDesaparecida
    context_object_name = "persona"

class EliminarPersonaDesaparecida(PermissionRequiredMixin,DeleteView): # Esta clase se utiliza para eliminar registros de las personas desaparecidas
    permission_required = 'localizacion_personas.delete_personadesaparecida' # Se especifica el registro necesario para acceder a esta vista
    model = PersonaDesaparecida
    success_url = reverse_lazy('localizacion_personas:lista')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '¡Registro eliminado exitosamente!')
        return super(EliminarPersonaDesaparecida, self).delete(request, *args, **kwargs)