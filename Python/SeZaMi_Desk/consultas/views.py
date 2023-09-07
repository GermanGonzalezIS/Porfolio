from django.shortcuts import render
from django.shortcuts import get_object_or_404

from tramites.models import Tramite
from beneficiarios.models import Beneficiario
from localizacion_personas.models import PersonaDesaparecida
from traslado_cuerpos.models import TrasladoCuerpo
from visas.models import Visa
from .forms import CurpForm, FolioForm
# Create your views here.

def index(request):
    form = CurpForm()
    formFolio = FolioForm()
    return render(request, 'index.html',{'form':form, 'formFolio':formFolio})

def lista(request):
    curp = request.POST['curp']
    try:
        beneficiario = Beneficiario.objects.filter(curp=curp).first()
        tramites = Tramite.objects.filter(beneficiario=beneficiario.curp)
        return render(request, 'lista_tramites.html',{'beneficiario':beneficiario,
                                                      'tramites':tramites,})
    except:
        return render(request, 'lista_tramites.html',{'curp':curp,})

def detalle(request,pk):
    try:
        tramite = Tramite.objects.filter(id=pk).first()
        beneficiario = tramite.beneficiario
        contacto = tramite.empleado
        nombre_contacto = contacto.first_name+" "+contacto.last_name
        return render(request, 'detalle.html',{'beneficiario':beneficiario,
                                               'tramite':tramite,
                                               'nombre_contacto':nombre_contacto,
                                               'telefono':contacto.telefono,})
    except:
        return render(request, 'detalle.html')

def detalleSolicitud(request):
    folio = request.POST['folio']
    try:
        solicitud = None
        tipoSolicitud = ""
        if int(folio) >= 100000000 and int(folio) < 200000000:
            solicitud = PersonaDesaparecida.objects.filter(folio=folio).first()
            tipoSolicitud = "Localizacion"
        elif int(folio) >= 200000000 and int(folio) < 300000000:
            solicitud = Visa.objects.filter(folio=folio).first()
            tipoSolicitud = "Visa"
        elif int(folio) >= 300000000:
            solicitud = TrasladoCuerpo.objects.filter(folio=folio).first()
            tipoSolicitud = "Traslado"
        contacto = solicitud.empleado
        nombre_contacto = contacto.first_name+" "+contacto.last_name
        return render(request, 'detalle_solicitud.html',{'solicitud':solicitud,
                                               'nombre_contacto':nombre_contacto,
                                               'telefono':contacto.telefono,'tipoSolicitud':tipoSolicitud,})
    except:
        return render(request, 'detalle_solicitud.html',{'folio':folio,})
