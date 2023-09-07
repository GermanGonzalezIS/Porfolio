from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest

from .views_pasaportes import crear_estudio_socioeconomico,crear_direccion
from .generar_curp.calcule import CalculeCURP
from pasaportes_seguros.models import Seguro
from tramites.forms import PedirCurpForm
from beneficiarios.models import Beneficiario, BeneficiarioDireccion, EstudioSocioeconomico
from beneficiarios.forms import BeneficiarioForm, BeneficiarioDireccionForm, EstudioSocioeconomicoForm
from tramites.models import Tramite, NombreTramites
from empleados.models import Empleado
from .forms import SeguroForm,GenerarCURPForm
from catalogos.forms import *

# Vista correspondiente a la lista de seguros.
class SegurosList(PermissionRequiredMixin,ListView):
    permission_required = 'pasaportes_seguros.view_seguro'
    # Modelo correspondiente.
    model = Seguro
    extra_context = { 'app' : 'seguros:lista',
                      'color' : '#6fb7cc' }
    # Template correspondiente.
    template_name = "seguros/seguro_list.html"

    def get(self,request,*args,**kwargs):
        tramite_seguro= NombreTramites.objects.get(id=4)
        user = request.user
        if user.is_superuser == 1:
            return super().get(request,*args,**kwargs)
        # Se obtiene el usuario logueado
        usuario = get_object_or_404(Empleado,username=request.user.username)
        # Se obtiene el grupo al que pertenece el usuario (Super Admin, Admin o Capturista)
        grupo_usuario = usuario.grupo.grupo
        if grupo_usuario == 'Super Administrador' or grupo_usuario == 'Administrador':
            # Es Super Admin o admin
            return super().get(request,*args,**kwargs)  
        else:
            # Es capturista, se muestran solamente los trámites que el usuario ha realizado
            print(usuario.id)
            print(tramite_seguro.id)
            lista_tramites = Tramite.objects.filter(Q(empleado=usuario.id) & Q(tipo_tramite=tramite_seguro.id))
            lista_seguros = []
            for tramite in lista_tramites:
                lista_seguros.append(Seguro.objects.get(tramite=tramite.id))
            print(lista_seguros)
            # Se obtiene asigna el context_object_name definido 
            self.object_list = lista_seguros
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            return self.render_to_response(context)

# Vista correspondiente al detalle de seguro.
class SeguroDetalle(PermissionRequiredMixin,DetailView):
    permission_required = 'pasaportes_seguros.view_seguro'
    # Modelo correspondiente.
    model = Seguro
    # Contexto que necesita el template.
    extra_context = { 'app' : 'seguros:lista',
                      'color' : '#6fb7cc' }
    # Template correspondiente.
    template_name = "seguros/seguro_detail.html"

# Vista correspondiente a la eliminación de seguro.
class SeguroEliminar(PermissionRequiredMixin,DeleteView):
    permission_required = 'pasaportes_seguros.delete_seguro'
    # Modelo correspondiente.
    model = Seguro
    # Se sobreescribe la función post.
    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de atencion_migrantes.
        tramite_id = kwargs['pk']
        # Se extrae el trámite correspondiente.
        tramite = get_object_or_404(Tramite,id=tramite_id)
        # Se elimina el trámite.
        tramite.delete()
        messages.success(self.request, '¡Registro eliminado exitosamente!')
        # Redirige a la lista de seguros.
        return redirect('seguros:lista')

# Vista correspondiente a la actualización de un seguro.
class SeguroActualizar(PermissionRequiredMixin,UpdateView):
    permission_required = 'pasaportes_seguros.change_seguro'
    # Modelo correspondiente.
    model = Seguro
    # Forms necesarios para el template.
    form_class = SeguroForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    form_beneficiario = BeneficiarioForm
    form_municipio = MunicipioForm
    form_localidad = LocalidadForm
    form_asentamiento = AsentamientoForm
    # Template correspondiente.
    template_name = "seguros/seguro_form.html"
    # Diccionario de contexto con las variables que necesita el tamplate.
    extra_context = {
        'etiqueta':'Actualizar', 
        'boton':'Guardar',
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
        'form_beneficiario':form_beneficiario,
        'form_municipio':form_municipio,
        'form_localidad':form_localidad,
        'form_asentamiento':form_asentamiento,
    }
    # Se sobreescribe la función get.
    def get(self,request,*args,**kwargs):
        # Se extrae el objeto correspondiente y el diccionario de conexto.
        self.object = self.get_object()
        seguro = self.object
        context = self.get_context_data()
        curp = seguro.curp 
        # Se busca si la curp correspondiente al objeto esta asociado a una entidad de
        # beneficiario previamente añadido.
        beneficiario = Beneficiario.objects.filter(curp=curp).first()
        # Si existe una entidad de beneficiario asociado al objeto.
        if beneficiario != None:
            # Los datos del beneficiario ya habían sido capturados, por lo tanto, se llenan
            # los campos del formulario automáticamente
            direccion = BeneficiarioDireccion.objects.filter(id=beneficiario.direccion_id).first()
            estudio = EstudioSocioeconomico.objects.filter(id=beneficiario.estudio_socioeconomico_id).first()
            form_beneficiario = BeneficiarioForm(instance=beneficiario)
            form_direccion = BeneficiarioDireccionForm(instance=direccion)
            form_estudio = EstudioSocioeconomicoForm(instance=estudio)
            # Se añade los formularios al contexto para ser usados en el template.
            context['form_beneficiario'] = form_beneficiario
            context['form_direccion'] = form_direccion
            context['form_estudio'] = form_estudio
            context['url_beneficiario'] = 'beneficiarios:editar' 
            context['id_beneficiario'] = curp 
        else:
            # Si no existe un beneficiario asociado al objeto se añade una url al contexto
            # que correspone a la creación de una nueva entidad de beneficiario.
            context['url_beneficiario'] = 'beneficiarios:crear' 
        context['app'] = 'seguros:lista'
        return self.render_to_response(context)

    # Se sobreescribe el método post.
    def post(self,request,*args,**kwargs):
        lista_documentos = ['years_work','years','numero_seguro_social','tramite']

        if all(documento in request.POST for documento in lista_documentos):
            # Todos los documentos del trámite fueron seleccionados.
            # Se guardan, y se continúa en la misma página para capturar
            # los datos del beneficiario
            return super().post(request,*args,**kwargs)
        else:
            # Faltaron documentos por seleccionar
            messages.success(request,'¡Trámite guardado!')
            super().post(request,*args,**kwargs)
            return redirect('seguros:lista')
        
    def get_success_url(self):
        return self.request.path

# Función correspondiente al template pedir_curp.html
def pedir_curp(request):
    # Si la petición es por método GET.
    if request.method == "GET":
        # Form correspondiente.
        form = PedirCurpForm()
        # Diccionario de contexto con las variables que necesita el template.
        extra_context = {'form':form,
                         'anterior':'seguros:lista',
                         'app':'seguros:verificar_curp',
                         'pasaportes_seguros': 'seguros:generar_curp'}
        # Direcciona al template pedir_curp.html.
        return render(request,'tramites/pedir_curp.html',extra_context)

# Función que verifica si la curp ya esta ingresada en el sistema.    
def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    # Se verficia si hay algún trámite ya registrado con esa curp
    tramites_registrados = Seguro.objects.filter(curp=curp)
    cant_tramites = tramites_registrados.count() # ...
    
    if cant_tramites == 0:
        # No existe ningún trámite con la CURP indicada, por lo tanto se 
        # crea uno nuevo
        tramite_seguro= NombreTramites.objects.get(id=4)
        # Creación del proceso trámite
        tramite = Tramite()
        tramite.estado_id = 1
        tramite.tipo_tramite = tramite_seguro
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
        seguro = Seguro()
        seguro.curp = curp
        seguro.tramite_id = tramite.id
        seguro.save()
        seguro = Seguro.objects.latest('id')
        return HttpResponseRedirect('/seguros/completar/' + str(seguro.id))
    else:
        # Ya existe un trámite con la CURP indicada
        tramite_seguro = tramites_registrados.first()
        tramite_general = Tramite.objects.filter(id=tramite_seguro.tramite_id).first()
        if tramite_general.estado_id == 1:
            id_pendiente = tramites_registrados.latest('id').id
            return HttpResponseRedirect('/seguros/completar/' + str(id_pendiente))
        else:
            # El trámite con la CURP indicada ya entregó toda la documentación necesaria y fueron
            # capturados los datos del beneficiario, por lo tanto el flujo de la aplicación reedirige
            # al usuario a la lista de trámites de 'Seguros...'
            messages.error(request,'Ya existe un trámite asociado a esta CURP')
            return redirect('seguros:lista')

def verificar_curp_generada(curp,nombre,primer_apellido,segundo_apellido,request):
    # Se verficia si hay algún trámite ya registrado con esa curp
    tramites_registrados = Seguro.objects.filter(curp=curp)
    cant_tramites = tramites_registrados.count() # ...
    
    if cant_tramites == 0:
        # No existe ningún trámite con la CURP indicada, por lo tanto se 
        # crea uno nuevo
        tramite_seguro = NombreTramites.objects.get(id=4)
        # Creación del proceso trámite
        tramite = Tramite()
        tramite.estado_id = 1
        tramite.tipo_tramite = tramite_seguro
        empleado = get_object_or_404(Empleado,username=request.user.username)
        tramite.empleado_id = empleado.id
        # Se verifica, en base a la CURP, si la información del beneficiario ya ha sido capturada.
        if Beneficiario.objects.filter(curp=curp).first() != None:
            # Los datos del beneficiario ya se encuentran capturados en el sistema
            # Se agrega la curp al proceso del trámite
            tramite.beneficiario_id = curp
        else:
            # Se crea un beneficiario con sus datos asi como su estudio socioeconómico y su dirección
            beneficiario = Beneficiario()
            beneficiario.curp=curp
            beneficiario.nombre=nombre
            beneficiario.primer_apellido=primer_apellido
            beneficiario.identificacion= get_object_or_404(IdentificacionOficial,identificacion='Otro')
            beneficiario.direccion = crear_direccion()
            beneficiario.estudio_socioeconomico = crear_estudio_socioeconomico()
            if(segundo_apellido!=None):
                beneficiario.segundo_apellido=segundo_apellido
            beneficiario.save()
            tramite.beneficiario_id = curp
        # Se guarda el tramite i se vuelve a extraer. 
        tramite.save()
        tramite = Tramite.objects.latest('id')

        # Creación trámite específico
        seguro = Seguro()
        seguro.curp = curp
        seguro.tramite_id = tramite.id
        seguro.save()
        seguro = Seguro.objects.latest('id')
        return HttpResponseRedirect('/seguros/completar/' + str(seguro.id))
    else:
        # Ya existe un trámite con la CURP indicada
        tramite_seguro = tramites_registrados.first()
        tramite_general = Tramite.objects.filter(id=tramite_seguro.tramite_id).first()
        if tramite_general.estado_id == 1:
            id_pendiente = tramites_registrados.latest('id').id
            return HttpResponseRedirect('/seguros/completar/' + str(id_pendiente))
        else:
            # El trámite con la CURP indicada ya entregó toda la documentación necesaria y fueron
            # capturados los datos del beneficiario, por lo tanto el flujo de la aplicación reedirige
            # al usuario a la lista de trámites de 'Pasaportes...'
            messages.error(request,'Ya existe un trámite asociado a esta CURP')
            return redirect('seguros:lista')

# Método que genera una CURP en caso de que el beneficiario no cuente con una.
def generar_curp(request):
    if request.method == "GET":
        #Si el método es GET se envia un formulario para ser llenado.
        form = GenerarCURPForm()
        extra_context = {'form':form,
                         'app':'seguros:lista'}
        return render(request,'generar_curp.html',extra_context)

    elif request.method == "POST":
        # Si el método es POST se extraen los datos del formulario.

        # Se le da un formato específico a la fecha.
        fecha = request.POST['fecha_nacimiento'].split('-')
        fecha_formateada = fecha[2]+'-'+fecha[1]+'-'+fecha[0]

        #Se extraen los demás datos.
        nombre = request.POST['nombre']
        primer_apellido = request.POST['primer_apellido']

        if (request.POST['segundo_apellido']==''):
            # Si el beneficiario no tiene segundo apellido.
            segundo_apellido=None
        else:
            # Si el beneficiario cuenta con segundo apellido.
            segundo_apellido=request.POST['segundo_apellido'] 

        # Se extraen los datos faltantes.
        sexo = request.POST['sexo']
        estado = request.POST['entidad']

        # Se colocan en un arreglo.
        datos = {
	        'fecha': fecha_formateada , 'nombres': nombre , 'paterno': primer_apellido ,
	        'materno': segundo_apellido , 'genero': sexo , 'estado': estado
        }
        # Se genera la curp.
        curp = CalculeCURP(**datos).data

        # Se manda llamar a la función encargada de verificar la curp generada. 
        return verificar_curp_generada(curp,nombre,primer_apellido,segundo_apellido,request)
