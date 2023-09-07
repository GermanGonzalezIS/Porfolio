from django.contrib import admin
from .models import Tramite,EstadoTramite,NombreTramites, Grupo, Club, Representante

admin.site.register(Tramite)
admin.site.register(Grupo)
admin.site.register(Representante)
admin.site.register(Club)
admin.site.register(EstadoTramite)
admin.site.register(NombreTramites)

