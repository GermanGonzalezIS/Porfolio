from django.db import models
from django.core.validators import RegexValidator

def autoincremento_folio(): 
    incremento = Visa.objects.all().order_by('folio').last()
    if not incremento:
        # Si la tabla no tiene registros regresamos el valor inicial del folio
        return 200000000 # 200000000 Es el valor inicial del folio
    return incremento.folio + 1

class Visa(models.Model):
    folio = models.IntegerField('folio',primary_key=True,default=autoincremento_folio)
    nombre_solicitante = models.CharField('Nombre',max_length=50, null=True, blank=False)
    apellido_paterno_solicitante = models.CharField('Apellido paterno',max_length=50, null=True, blank=False)
    apellido_materno_solicitante = models.CharField('Apellido materno',max_length=50,blank=True, null=True)
    pasaporte = models.BooleanField('Pasaporte',default=False)
    direccion_usa = models.CharField('Dirección de Estados Unidos',max_length=70, null=True)
    persona_visitar = models.CharField('Nombre de la persona a visitar',max_length=70, null=True)
    tel_persona_visitar = models.CharField('Teléfono de la persona a visitar',max_length=15,validators=[RegexValidator('\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$')], null=True)
    fe_nacimiento_madre = models.DateField('Fecha de nacimiento de la madre', null=True)
    fe_nacimiento_padre = models.DateField('Fecha de nacimiento del padre', null=True)
    dir_trabajo_escuela = models.CharField('Dirección del lugar de trabajo o escuela',max_length=80, null=True)
    nom_dir_trabajo_escuela = models.CharField('Nombre de la dirección del trabajo o escuela',max_length=35, null=True)
    fe_ingreso_trabajo_escuela = models.DateField('Fecha de ingreso al trabajo o escuela', null=True)
    ingreso_mensual = models.DecimalField('Ingreso Mensual',max_digits=10, decimal_places=2, null=True)
    fecha_viaje = models.DateField('Fecha tentativa de viaje', null=True)
    red_social_uno = models.CharField('Red social 1',max_length=30,blank=True, null=True)
    usuario_uno = models.CharField('Nombre de usuario',max_length=30,blank=True, null=True)
    red_social_dos = models.CharField('Red social 2',max_length=30,blank=True, null=True)
    usuario_dos = models.CharField('Nombre de usuario',max_length=30,blank=True, null=True)
    red_social_tres = models.CharField('Red social 3',max_length=30,blank=True, null=True)
    usuario_tres = models.CharField('Nombre de usuario',max_length=30,blank=True, null=True)
    correo = models.EmailField('Correo electrónico', null=True)
    pago = models.BooleanField(default=False)
    empleado = models.ForeignKey("empleados.Empleado",verbose_name='Empleado',on_delete=models.CASCADE)
    fecha_cita = models.DateField('Fecha de la cita en el consulado',null=True,blank=True)

    corazon_plata = models.ForeignKey("corazon_plata.CorazonPlata", verbose_name="Trámite de Corazón de Plata", on_delete=models.CASCADE, null=True, blank=True)