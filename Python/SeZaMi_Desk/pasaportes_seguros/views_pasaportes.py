from django import http
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpRequest, request

from .generar_curp.calcule import CalculeCURP
from pasaportes_seguros.models import Pasaporte
from .forms import GenerarCURPForm, PasaporteForm
from beneficiarios.models import Beneficiario, BeneficiarioDireccion, EstudioSocioeconomico
from beneficiarios.forms import BeneficiarioForm, BeneficiarioDireccionForm, EstudioSocioeconomicoForm
from tramites.forms import PedirCurpForm
from tramites.models import Tramite, NombreTramites
from empleados.models import Empleado
from catalogos.forms import *
from catalogos.models import IdentificacionOficial

@login_required
# Función que dirige al template de inicio.
def inicio_servicio(request):
    return render(request,'pasaportes_seguros_principal.html')

# Método quue crea una dirección para un beneficiario.
def crear_direccion():
    direccion = BeneficiarioDireccion()
    direccion.tipo_vialidad = get_object_or_404(TipoVialidad,vialidad='Calle')
    direccion.numero_exterior = 0
    direccion.municipio = get_object_or_404(Municipio,municipio='Otro')
    direccion.localidad = get_object_or_404(Localidad,localidad='Otro')
    direccion.asentamiento = get_object_or_404(Asentamiento,asentamiento='Otro')
    direccion.save()
    return direccion

# Método que crea un estudio socioeconómico para un beneficiario.
def crear_estudio_socioeconomico():
    estudio = EstudioSocioeconomico()
    estudio.estudio_socioeconomico = True
    estudio.estado_civil = get_object_or_404(EstadoCivil,estado_civil='Soltero(a)')
    estudio.jefe_familia = False
    estudio.ocupacion = get_object_or_404(Ocupacion,ocupacion='Oficio varios')
    estudio.ingreso_mensual = get_object_or_404(IngresoMensual,descripcion='Ninguno')
    estudio.integrantes_familia = 0
    estudio.dependientes_economicos = 0
    estudio.vivienda = get_object_or_404(Vivienda,vivienda='Casa propia')
    estudio.numero_habitantes_vivienda = 0
    estudio.nivel_estudios = get_object_or_404(NivelEstudios,nivel_estudio='Ninguno')
    estudio.tipo_seguridad_social = get_object_or_404(TipoSeguridadSocial,seguridad_social='Ninguno')
    estudio.discapacidad = get_object_or_404(Discapacidad,discapacidad='Ninguna')
    estudio.grupo_vulnerable = get_object_or_404(GrupoVulnerable,grupo_vulnerable='Ninguno')
    estudio.save()
    return estudio

# Vista correspondiente a la lista de pasaportes.
class PasaportesList(PermissionRequiredMixin,ListView):
    permission_required = 'pasaportes_seguros.view_pasaporte'
    # Modelo correspondiente.
    model = Pasaporte
    extra_context = { 'app' : 'pasaportes:lista',
                      'color' : '#b68ab6' }
    # Template correspondiente.
    template_name = "pasaportes/pasaporte_list.html"

    def get(self,request,*args,**kwargs):
        tramite_pasaporte = NombreTramites.objects.get(id=3)
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
            lista_tramites = Tramite.objects.filter(Q(empleado_id=usuario.id) & Q(tipo_tramite=tramite_pasaporte.id))
            lista_pasaportes = []
            for tramite in lista_tramites:
                lista_pasaportes.append(Pasaporte.objects.get(tramite=tramite.id))
            # Se obtiene asigna el context_object_name definido 
            self.object_list = lista_pasaportes
            # Se agregan los trámites filtrados a la lista de variables a pasar al template
            context = self.get_context_data()
            return self.render_to_response(context)

# Vista correspondiente al detalle de pasaporte.
class PasaporteDetalle(PermissionRequiredMixin,DetailView):
    permission_required = 'pasaportes_seguros.view_pasaporte'
    # Modelo correspondiente.
    model = Pasaporte
    # Diccionario de contexto con la variable que necesita el template.
    extra_context = { 'app' : 'pasaportes:lista',
                      'color' : '#b68ab6' }
    # Template correspondiente.
    template_name = "pasaportes/pasaporte_detail.html"

# Vista correspondiente a la eliinación de un pasaporte.
class PasaporteEliminar(PermissionRequiredMixin,DeleteView):
    permission_required = 'pasaportes_seguros.delete_pasaporte'
    # Modelo correspondiente.
    model = Pasaporte 

    # Se sobreescribe la funcion post.
    def post(self,request,*args,**kwargs):
        # Se elimina el proceso del tramite que internamente elimina el
        # registro en la tabla de atencion_migrantes
        tramite_id = kwargs['pk']
        # Se extrae el trámite correspondiente.
        tramite = get_object_or_404(Tramite,id=tramite_id)
        # se elimina el trámite correspondiente.
        tramite.delete()
        messages.success(self.request, '¡Registro eliminado exitosamente!')
        # Redirecciona la la lista de pasaportes.
        return redirect('pasaportes:lista')

# Vista correspondiente a la creación de un nuevo pasaporte.
class PasaporteNuevo(PermissionRequiredMixin,CreateView):
    permission_required = 'pasaportes_seguros.add_pasaporte'
    # Modelo correspondiente.
    model = Pasaporte
    # Forms necesarios para el template.
    form_class = PasaporteForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    form_beneficiario = BeneficiarioForm
    # Template correspondiente.
    template_name = "pasaportes/pasaporte_form.html"
    # Diccionario de contexto con las variables que necesita el tamplate.
    extra_context = {
        'etiqueta':'Nuevo', 
        'boton':'Agregar', 
        'form_direccion':form_direccion,
        'form_estudio':form_estudio,
        'form_beneficiario':form_beneficiario,
    }
    # Si la operación tuvo exito se redireccionará a la lista de pasaportes.
    success_url = reverse_lazy('pasaportes:lista')

# Vista correspondiente a la actualización de un pasaporte.
class PasaporteActualizar(PermissionRequiredMixin,UpdateView):
    permission_required = 'pasaportes_seguros.change_pasaporte'
    # Modelo correspondiente.
    model = Pasaporte
    # Forms necesarios para el template.
    form_class = PasaporteForm
    form_direccion = BeneficiarioDireccionForm
    form_estudio = EstudioSocioeconomicoForm
    form_beneficiario = BeneficiarioForm
    form_municipio = MunicipioForm
    form_localidad = LocalidadForm
    form_asentamiento = AsentamientoForm
    # Template correspondiente.
    template_name = "pasaportes/pasaporte_form.html"
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
        pasaporte = self.object
        context = self.get_context_data()
        curp = pasaporte.curp 
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
        context['app'] = 'pasaportes:lista'
        return self.render_to_response(context)

    # Se sobreescribe el método post.
    def post(self,request,*args,**kwargs):
        lista_documentos = ['acta','seguro_social','identificacion_padres']

        if all(documento in request.POST for documento in lista_documentos) and request.POST['nombre_contacto_usa']!='' and request.POST['direccion_usa']!='' and request.POST['tel_contacto_usa']!='' and request.POST['correo']!='':
            # Todos los documentos del trámite fueron seleccionados.
            # Se guardan, y se continúa en la misma página para capturar
            # los datos del beneficiario
            return super().post(request,*args,**kwargs)
        else:
            # Faltaron documentos por seleccionar
            messages.success(request,'¡Trámite guardado!')
            print(str(request.POST))
            super().post(request,*args,**kwargs)
            return redirect('pasaportes:lista')
        
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
                         'anterior':'pasaportes:lista',
                         'app':'pasaportes:verificar_curp',
                         'pasaportes_seguros': 'pasaportes:generar_curp'}
        # Direcciona al template pedir_curp.html.
        return render(request,'tramites/pedir_curp.html',extra_context)

def verificar_curp(request):
    # Se obtiene la CURP ingresada por el usuario
    curp = request.POST['curp']
    # Se verficia si hay algún trámite ya registrado con esa curp
    tramites_registrados = Pasaporte.objects.filter(curp=curp)
    cant_tramites = tramites_registrados.count() # ...
    
    if cant_tramites == 0:
        # No existe ningún trámite con la CURP indicada, por lo tanto se 
        # crea uno nuevo
        tramite_pasaporte = NombreTramites.objects.get(id=3)
        # Creación del proceso trámite
        tramite = Tramite()
        tramite.estado_id = 1
        tramite.tipo_tramite = tramite_pasaporte
        empleado = get_object_or_404(Empleado,username=request.user.username)
        tramite.empleado_id = empleado.id
        # Se verifica, en base a la CURP, si la información del beneficiario ya ha sido capturada.
        if Beneficiario.objects.filter(curp=curp).first() != None:
            # Los datos del beneficiario ya se encuentran capturados en el sistema
            # Se agrega la curp al proceso del trámite
            tramite.beneficiario_id = curp
                
        # Se guarda el tramite i se vuelve a extraer. 
        tramite.save()
        tramite = Tramite.objects.latest('id')

        # Creación trámite específico
        pasaporte = Pasaporte()
        pasaporte.curp = curp
        pasaporte.tramite_id = tramite.id
        pasaporte.save()
        pasaporte = Pasaporte.objects.latest('id')
        return HttpResponseRedirect('/pasaportes/completar/' + str(pasaporte.id))
    else:
        # Ya existe un trámite con la CURP indicada
        tramite_pasaporte = tramites_registrados.first()
        tramite_general = Tramite.objects.filter(id=tramite_pasaporte.tramite_id).first()
        if tramite_general.estado_id == 1:
            id_pendiente = tramites_registrados.latest('id').id
            return HttpResponseRedirect('/pasaportes/completar/' + str(id_pendiente))
        else:
            # El trámite con la CURP indicada ya entregó toda la documentación necesaria y fueron
            # capturados los datos del beneficiario, por lo tanto el flujo de la aplicación reedirige
            # al usuario a la lista de trámites de 'Pasaportes...'
            print(str(request.body))
            messages.error(request,'Ya existe un trámite asociado a esta CURP')
            return redirect('pasaportes:lista')

def verificar_curp_generada(curp,nombre,primer_apellido,segundo_apellido,request):
    # Se verficia si hay algún trámite ya registrado con esa curp
    tramites_registrados = Pasaporte.objects.filter(curp=curp)
    cant_tramites = tramites_registrados.count() # ...
    
    if cant_tramites == 0:
        # No existe ningún trámite con la CURP indicada, por lo tanto se 
        # crea uno nuevo
        tramite_pasaporte = NombreTramites.objects.get(id=3)
        # Creación del proceso trámite
        tramite = Tramite()
        tramite.estado_id = 1
        tramite.tipo_tramite = tramite_pasaporte
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
        pasaporte = Pasaporte()
        pasaporte.curp = curp
        pasaporte.tramite_id = tramite.id
        pasaporte.save()
        pasaporte = Pasaporte.objects.latest('id')
        return HttpResponseRedirect('/pasaportes/completar/' + str(pasaporte.id))
    else:
        # Ya existe un trámite con la CURP indicada
        tramite_pasaporte = tramites_registrados.first()
        tramite_general = Tramite.objects.filter(id=tramite_pasaporte.tramite_id).first()
        if tramite_general.estado_id == 1:
            id_pendiente = tramites_registrados.latest('id').id
            return HttpResponseRedirect('/pasaportes/completar/' + str(id_pendiente))
        else:
            # El trámite con la CURP indicada ya entregó toda la documentación necesaria y fueron
            # capturados los datos del beneficiario, por lo tanto el flujo de la aplicación reedirige
            # al usuario a la lista de trámites de 'Pasaportes...'
            print("entre")
            messages.error(request,'Ya existe un trámite asociado a esta CURP')
            return redirect('pasaportes:lista')

# Método que genera una CURP en caso de que el beneficiario no cuente con una.
def generar_curp(request):
    if request.method == "GET":
        #Si el método es GET se envia un formulario para ser llenado.
        form = GenerarCURPForm()
        extra_context = {'form':form,
                         'app':'pasaportes:lista'}
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


