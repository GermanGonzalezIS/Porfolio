from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.urls.base import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView,UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from .cifrado import cifrar, descifrar
from empleados.models import Empleado,Grupo
from .forms import EmpleadoForm,EmpleadoModificarForm
from .models import Empleado

# Clase correspondiete a la lista de empleados.
class EmpleadoList(PermissionRequiredMixin,ListView):
    # Permiso requerido para acceder a esta vista.
    permission_required = 'empleados.view_empleado'
    model = Empleado   

# Clase correspondiente a la creación de un nuevo objeto de tipo Empleado.
class NuevoEmpleado(PermissionRequiredMixin,CreateView):
    # Permiso requerido para acceder a esta vista.
    permission_required = 'empleados.add_empleado'
    model = Empleado
    form_class = EmpleadoForm
    extra_context = {'etiqueta':'Nuevo','btn':'Agregar'} 

    # Función que indica a donde nod enviará la plicación después de que se realizará la operación exitosamente. 
    def get_success_url(self):
        return reverse('empleados:permisos',args=(self.object.id,))

    # Funcion que guarda el nuevo objeto
    def form_valid(self, form):
        # Se guarda el formulario como nuevo Empleado y se le asigna a la variable user.
        user = form.save(commit=False)
        # A la variable user de tipo Empleado se le asigna su campo "contra"
        user.contra = cifrar(self.request.POST['password'])
        # Se manda llamar a la función original de la clase CreateView.
        return super().form_valid(form)

# Clase correspondiente a la eliminación de un registro de Empleado.
class EliminarEmpleado(PermissionRequiredMixin,DeleteView):
    # Permiso requerido para acceder a esta vista.
    permission_required = 'empleados.delete_empleado'
    model = Empleado
    success_url=reverse_lazy('empleados:lista')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '¡Usuario eliminado exitosamente!')
        return super(EliminarEmpleado, self).delete(request, *args, **kwargs)

# Clase correspondiente a la modificación de un registro de Empleado.
class ModificarEmpleado(PermissionRequiredMixin,UpdateView):
    # Permiso requerido para acceder a esta vista.
    permission_required = 'empleados.change_empleado'
    model = Empleado
    form_class = EmpleadoModificarForm
    extra_context = {'etiqueta':'Modificar','btn':'Guardar'}
    success_url = reverse_lazy('empleados:lista')

    # Se sobreescribe el método perteneciente a la clase UpdateView.
    def get_object(self, queryset=None):
        # Se manda llamar al método original de la clase UpdateView.
        empleado = super().get_object()
        # Se descifra la contraseña.
        empleado.contra = descifrar(empleado.contra)
        # Regresa el objeto empleado.
        return empleado
    
    def form_valid(self, form):
        # Se modifica el Empleado con el formulario y se le asigna a la variable user.
        user = form.save(commit=False)
        # A la variable user de tipo Empleado se le asigna el nuevo valor cifrado para "contra".
        user.contra = cifrar(self.request.POST['contra'])
        # Se manda llamar a la función original de la clase Updateview.
        messages.success(self.request, '¡Usuario modificado exitosamente!')
        return super().form_valid(form)

# Función correspondiente al login de los usuarios.
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username=username, password=password)
    
        if usuario is not None:
            if usuario.is_active:
                auth_login(request, usuario)
                return redirect('tramites:lista_tramite')
        else:
            messages.error(request,'El usuario o la contraseña no son correctos')
            return redirect('empleados:login')
    
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Clase correspondiente al logout de los usuarios.
class EmpleadoLogout(LogoutView):
    template_name='login.html'

# Función correspondiente a ver los datos del usuario logeado.
# Permiso que se requiere (haber iniciado sesión)
@login_required
def verPerfil(request):
    # Se extrae el objeto Empleado de la base de datos correspondiete al usuario logeado.
    empleado = get_object_or_404(Empleado,pk=request.user.id)
    empleado.contra = descifrar(empleado.contra)
    # Se extrae los grupos a los que el usuario pertenece.
    # Estos grupos se extraen de la tabla Groups del apartado de Autenticación y Autorización no del apartado de la aplicación Empleados.
    permisos = empleado.groups.all()
    # Se extrae el grupo del empleado.
    # Este grupo se extrae de la tabla Grupos perteneciente al apartado de la aplicación Empleados (Super Admin, Admin, Capturista).
    grupo = get_object_or_404(Grupo,grupo=empleado.grupo)
    # Mensaje que se mostrara en el template si el usuario es Super Admin.
    admin ='El empleado es super administrador'
    # Si el usuario pertenece al grupo Super Admin.
    if (grupo.grupo.lower() == "super administrador"):
        # Direcciona al template perfil con las variables por contexto necesarias.
        return render(request, 'perfil.html',{'permisos':permisos,
                                            'empleado':empleado,
                                            'admin':admin})    
    # Direcciona al template perfil con las variables por contexto necesarias.
    return render(request, 'perfil.html',{'permisos':permisos,
                                            'empleado':empleado,})

# Función correspondiente a exraer los grupos del apartado de Autenticación y Autorización y a los que el usuario pertenece.
# Permiso que se requiere (haber iniciado sesión)
@login_required
@permission_required('empleados.add_empleado', raise_exception=True)
def permisos(request, pk):
    # Se extrae el objeto Empleado de la base de datos.
    empleado = get_object_or_404(Empleado,pk=pk)
    # Se extrae el grupo del empleado.
    # Este grupo se extrae de la tabla Grupos perteneciente al apartado de la aplicación Empleados (Super Admin, Admin, Capturista).
    grupo = get_object_or_404(Grupo,grupo=empleado.grupo)
    # Si el empleado pertenece al grupo Super Admin
    if (grupo.grupo.lower()=="super administrador"):
        # Llama a la función guardarSuperAdmin
        guardarSuperAdmin(empleado,grupo)
        # Redirecciona a la vista de la lista de empleados.
        return redirect('empleados:lista')
    # Extrae todos los grupos del apartado de Autenticación y Autorización.
    groups = Group.objects.all()
    # Extrae todos los grupos a los que el usuario pertenece.
    grupos_empleado = empleado.groups.all()
    # Crea una lista llamada permisos.
    permisos=[]
    # Iterar cada grupo en groups.
    for group in groups:
        # Se divide el nombre del grupo por espacios.
        p = group.name.split(" ")
        # Si el permiso pertenece al grupo. La primera palabra de cada permiso debe ser Admin o Capturista.
        if(grupo.grupo.lower()==p[0].lower()):
            # Se agrega el permiso a la lista.
            permisos.append(group)
    # Se direciona al template lista_permisos.html con las variables necesarias.
    return render(request, 'lista_permisos.html',{'permisos':permisos,
                                                   'grupo':grupo,
                                                   'empleado':empleado,
                                                   'grupos_empleado':grupos_empleado})

# Función correspondiente a agregar los permisos seleccionados en el template lista_permisos.html.
# Permiso que se requiere (haber iniciado sesión).
# Se requiere tener el permiso de empleados.add_empleado.
@login_required
@permission_required('empleados.add_empleado', raise_exception=True)
def agregaPermiso(request, pk):
    # Se estrae el objeto de tipo Empleado.
    empleado = Empleado.objects.get(id=pk)
    # Se extrae el id del grupo del formulario (Super Admin, Admin, Capturista).
    grupo_id=int(request.POST['grupo'])
    # Se extrae el grupo correspondiente al id extraido del formulario (Super Admin, Admin, Capturista).
    grupo = Grupo.objects.get(id=grupo_id)
    # El empleado se agrega a este grupo.
    empleado.grupo=grupo
    # Se guarda el empleado en la base de datos.
    empleado.save()
    # Se eliminan todos los permisos del empleado.
    empleado.groups.clear()
    # Se itera cada item del formulario.
    for item in request.POST:
        # Si el item del formulario se encuetra encendido.
        if request.POST[item] == 'on':
            # Se agrega el permiso correspondiente a ese item.
            empleado.groups.add(Group.objects.get(id=int(item)))
    # Se redirecciona a la lista de los empleados.
    messages.success(request, '¡Usuario registrado exitosamente!')
    return redirect('empleados:lista')

# Función correspondiente a extraer los datos de un empleado.
# Permiso que se requiere (haber iniciado sesión).
# Se requiere tener el permiso de empleados.view_empleado.
@login_required
@permission_required('empleados.view_empleado', raise_exception=True)
def detalleEmpleado(request,pk):
    # Se estrae el objeto de tipo Empleado.
    empleado = get_object_or_404(Empleado,pk=pk)
    empleado.contra = descifrar(empleado.contra)
    # Se extrae los permisos del usuario.
    grupos = empleado.groups.all()
    # Mensaje a mostrar si el usuario es Super Admin
    admin ='El empleado es super administrador'
    # Se iteran los permisos del usuario.
    for grupo in grupos:
        # Si el usuario es Super Admin.
        if (grupo.name.lower()=='super administrador'):
            # Se direcciona al template empleado_detail.html con las variables necesarias.
            return render(request, 'empleado_detail.html',{'permisos':grupos,
                                                           'empleado':empleado,
                                                           'admin':admin})
    # Se direcciona al template empleado_detail.html con las variables necesarias.
    return render(request, 'empleado_detail.html',{'permisos':grupos,
                                                   'empleado':empleado})

# Función correspondiente a extraer al empleado y los grupos (Super Admin, Admin, Capturista).
# Permiso que se requiere (haber iniciado sesión).
# Se requiere tener el permiso de empleados.change_empleado.
@login_required
@permission_required('empleados.change_empleado', raise_exception=True)                                                
def seleccionaGrupo(request,pk):
    # Se estrae el objeto de tipo Empleado.
    empleado = get_object_or_404(Empleado,pk=pk)
    # Se extrae los permisos del usuario.
    grupos = Grupo.objects.all()
    # Direcciona al template empleado_grupo.html con las variables correspondientes.
    return render(request, 'empleado_grupo.html',{'grupos':grupos,
                                                   'empleado':empleado})

# Función correspondiente a extraer los permisos correspondienes según el grupo al que pertenezca el empleado (Super Admin, Admin, Capturista).
# Permiso que se requiere (haber iniciado sesión).
# Se requiere tener el permiso de empleados.change_empleado.
@login_required
@permission_required('empleados.change_empleado', raise_exception=True)
def seleccionarPermisos(request):
    # Se extrae el Empleado correspondiente.
    empleado=Empleado.objects.get(pk=int(request.POST['empleado']))
    # Se extrae el id del grupo al que se desea agregar al empleado. 
    id_grupo=int(request.POST['select'])
    # Se extrae el objeto de tipo Grupo correspondiente al id.
    grupo = Grupo.objects.get(id=id_grupo)
    # Si el emleado se desea agregar al grupo de Super Admin.
    if (grupo.grupo.lower()=="super administrador"):
        # Se manda llamar a la función que añade los permisos de Super Admin al Empleado.
        guardarSuperAdmin(empleado,grupo)
        # Se redirige a la vista correspondiente a la lista de empleados.
        return redirect('empleados:lista')
    # Se extraen los grupos a los que el empleado pertenece actualmente.
    grupos_empleado = empleado.groups.all()
    # Se extraen todos los grupos.
    groups = Group.objects.all()
    # Se inicializa una arreglo que contendrá los permisos correspondientes al grupo (Admin, Capturista).
    permisos=[]
    # Se iteran los grupos.
    for group in groups:
        # Se separa el nombre de los grupos.
        p = group.name.split(" ")
        # Si el nombre del grupo es igual al del permiso.
        if(grupo.grupo==p[0]):
            # Se añade a permisos.
            permisos.append(group)
    # Envía al template lista_permisos.html con las variables necesarias.
    return render(request, 'lista_permisos.html',{'permisos':permisos,
                                                   'grupo':grupo,
                                                   'empleado':empleado,
                                                   'grupos_empleado':grupos_empleado,
                                                   'modificar':1})

# Función correspondiente a añadir los permisos de Super Admin.
def guardarSuperAdmin(empleado,grupo):
    # Se le setea el grupo de Super Admin.
    empleado.grupo=grupo
    # Se guarda al empleado.
    empleado.save()
    # Se eliminan todos sus permisos.
    empleado.groups.clear()
    # Se le añaden los permisos correspondientes al Super Admin.
    empleado.groups.add(Group.objects.get(name=grupo.grupo))