from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.http import JsonResponse

from .models import Municipio, Localidad, Asentamiento

# Create your views here.
class CatalogoGeneral(TemplateView):
    template_name = 'base.html'

def obtener_localidades(request):
    if request.method == 'GET':
        return JsonResponse({'error':'Petición incorrecta'}, safe=False, status=403)
    id_municipio = request.POST.get('id')
    localidades = Localidad.objects.filter(municipio_id=id_municipio)
    json = []
    if not localidades:
        json.append({'error' : '---------'})
    for localidad in localidades:
        json.append({'id' : localidad.id,
                     'nombre' : localidad.localidad})
    return JsonResponse(json, safe=False)

def obtener_asentamientos(request):
    if request.method == 'GET':
        return JsonResponse({'error':'Petición incorrecta'}, safe=False, status=403)
    id_localidad = request.POST.get('id')
    asentamientos = Asentamiento.objects.filter(localidad_id=id_localidad)
    json = []
    if not asentamientos:
        json.append({'error' :'---------'})
    for asentamiento in asentamientos:
        json.append({'id' : asentamiento.id,
                     'nombre' : asentamiento.asentamiento})
    return JsonResponse(json, safe=False)

def obtener_municipios(request):
    if request.method == 'GET':
        return JsonResponse({'error':'Petición incorrecta'}, safe=False, status=403)
    municipios = Municipio.objects.all()
    json = []
    for municipio in municipios:
        json.append({'id' : municipio.id,
                     'nombre' : municipio.municipio})
    return JsonResponse(json, safe=False)