from django.db import models
from django.core.validators import RegexValidator

def autoincremento_folio(): 
    incremento = DobleNacionalidad.objects.all().order_by('folio').last()
    if not incremento:
        # Si la tabla no tiene registros regresamos el valor inicial del folio
        return 400000000 # 100000000 Es el valor inicial del folio
    return incremento.folio + 1

class DobleNacionalidad(models.Model):
    folio = models.IntegerField('folio', primary_key=True, default=autoincremento_folio)
    nombre = models.CharField('Nombre',max_length=50)
    apellido_paterno = models.CharField('Apellido paterno',max_length=50)
    apellido_materno = models.CharField('Apellido materno',max_length=50,blank=True, null=True)
    acta_nacimiento_original = models.BooleanField("Acta de Nacimiento Original",default=False)
    actas_apostilladas = models.BooleanField("Actas apostilladas",default=False)
    comprobante_domicilio = models.BooleanField("Comprobante de domicilio",default=False)
    identificacion_oficial = models.BooleanField("Identificación Oficial Padres",default=False)
    original_copias = models.BooleanField("Original y 2 Copias tama",default=False) 
    tramite_estado = models.ForeignKey('tramites.EstadoTramite',verbose_name='Estado trámite',on_delete=models.CASCADE, null=True)   
    empleado = models.ForeignKey("empleados.Empleado",verbose_name='Empleado',on_delete=models.CASCADE)
