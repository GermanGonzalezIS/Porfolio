from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('consultas.urls')),
    path('apostillas/',include('apostillas.urls')),
    path('tramites/',include('tramites.urls')),
    path('beneficiarios/', include('beneficiarios.urls')),
    path('empleados/',include('empleados.urls')),
    path('localizacion-personas/',include('localizacion_personas.urls')),
    path('atencion-migrantes/',include('atencion_migrantes.urls')),
    path('visas/',include('visas.urls')),
    path('corazon-plata/',include('corazon_plata.urls')),
    path('catalogos/',include('catalogos.urls')),
    path('pasaportes/',include('pasaportes_seguros.urls_pasaportes')),
    path('seguros/',include('pasaportes_seguros.urls_seguros')),
    path('traslado-cuerpos/',include('traslado_cuerpos.urls')),

    #Ferias binacionales
    path('constancia-estudios/',include('constancia_estudio.urls')),
    path('licencia-conducir/',include('licencia_conducir.urls')),
    path('mandamientos-judiciales/',include('mandamientos_judiciales.urls')),
    path('defensoria-publica/',include('defensoria_publica.urls')),
    path('correccion-acta/',include('correccion_acta.urls')),
    path('expedicion-acta/',include('expedicion_acta.urls')),
    path('doble-nacionalidad/',include('doble_nacionalidad.urls')),

]
