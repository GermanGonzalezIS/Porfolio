from django.db import models
from django.core.validators import RegexValidator

def autoincremento_folio(): 
    incremento = TrasladoCuerpo.objects.all().order_by('folio').last()
    if not incremento:
        # Si la tabla no tiene registros regresamos el valor inicial del folio
        return 300000000 # 300000000 Es el valor inicial del folio
    return incremento.folio + 1

# Create your models here.
class TrasladoCuerpo(models.Model):
    folio = models.IntegerField('folio',primary_key=True,default=autoincremento_folio)
    nombre_fallecido = models.CharField('Nombre del fallecido',max_length=70)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    fecha_deceso = models.DateField('Fecha de deceso')
    causa_muerte = models.CharField('Causa de la muerte',max_length=50)
    lugar_deceso = models.CharField('Lugar del deceso',max_length=40)
    lugar_origen = models.CharField('Lugar de origen',max_length=40)
    anios_en_eu = models.PositiveIntegerField('Años',default=0)
    meses_en_eu = models.PositiveIntegerField('Meses',default=0)
    situacion_migratoria = models.ForeignKey('traslado_cuerpos.SituacionMigratoria',verbose_name='Situación Migratoria',on_delete=models.CASCADE)
    nombre_familiar_mexicano = models.CharField('Nombre del familiar en México',max_length=70)
    telefono = models.CharField('Teléfono',max_length=15,validators=[RegexValidator('\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$')])
    empleado = models.ForeignKey("empleados.Empleado",verbose_name='Empleado',on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_fallecido

class SituacionMigratoria(models.Model):
    situacion = models.CharField('Situación Migratoria',max_length=20)

    def __str__(self):
        return self.situacion