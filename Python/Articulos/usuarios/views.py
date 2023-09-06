from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from .models import Usuario
from .forms import UsuarioForm


# Create your views here.
class UsuarioList(ListView):

    model = Usuario


class UsuarioNuevo(CreateView):

    model = Usuario
    form_class = UsuarioForm
    extra_context = {'lista_grupos': Group.objects.all(),
                     'titulo': 'Nuevo usuario'}
    success_message = "Usuario creado correctamente"

    def form_valid(self, form):

        user = form.save(commit=True)
        user.groups.clear()
        for item in self.request.POST:

            if self.request.POST[item] == 'on':

                user.groups.add(Group.objects.get(id=int(item)))
        user.save()
        return super().form_valid(form)

    def get_success_url(self):

        return reverse('usuarios:lista')


def login(request):

    if request.method == 'POST':

        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username=username, password=password)

        if usuario is not None:

            if usuario.is_active:

                auth_login(request, usuario)
                return redirect('publicaciones:inicio')
        else:

            messages.error(request,
                           'El usuario o la contraseña no son correctos')
            return redirect('usuarios:login')
    else:

        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


class UsuarioEliminar(DeleteView):

    model = Usuario
    success_url = reverse_lazy('usuarios:lista')

    def delete(self, request, *args, **kwargs):

        messages.success(self.request, '¡Usuario eliminado exitosamente!')
        return super(UsuarioEliminar, self).delete(request, *args, **kwargs)


def usuario_modificar(request, pk):

    usuario = Usuario.objects.get(id=pk)
    form = UsuarioForm(instance=usuario)
    grupos_usuario = usuario.groups.all()
    if (request.method == 'POST'):

        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():

            usuario = form.save(commit=True)
            usuario.groups.clear()
            for item in request.POST:

                if request.POST[item] == 'on':

                    usuario.groups.add(Group.objects.get(id=int(item)))
            usuario.save()
            return redirect('usuarios:lista')
    context = {'form': form,
               'grupos_usuario': grupos_usuario,
               'lista_grupos': Group.objects.all(),
               'titulo': 'Modificar usuario'}
    return render(request, 'usuarios/usuario_form.html', context)


def usuario_detalle(request, pk):

    usuario = get_object_or_404(Usuario, id=pk)
    grupos = usuario.groups.all()
    return render(request, 'usuarios/usuario_detail.html',
                  {'permisos': grupos,
                   'usuario': usuario})
