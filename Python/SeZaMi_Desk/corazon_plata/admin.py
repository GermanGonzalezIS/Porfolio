from django.contrib import admin
from .models import GrupoVisa, Federaciones, CorazonPlata

# Register your models here.
admin.site.register(CorazonPlata)
admin.site.register(GrupoVisa)
admin.site.register(Federaciones)

