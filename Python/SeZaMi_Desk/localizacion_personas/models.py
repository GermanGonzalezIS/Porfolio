from django.db import models
from django.core.validators import RegexValidator

def autoincremento_folio(): 
    incremento = PersonaDesaparecida.objects.all().order_by('folio').last()
    if not incremento:
        # Si la tabla no tiene registros regresamos el valor inicial del folio
        return 100000000 # 100000000 Es el valor inicial del folio
    return incremento.folio + 1

class PersonaDesaparecida(models.Model):
    folio = models.IntegerField('folio', primary_key=True, default=autoincremento_folio)
    nombre_desaparecido = models.CharField('Nombre',max_length=50)
    apellido_paterno_desaparecido = models.CharField('Apellido paterno',max_length=50)
    apellido_materno_desaparecido = models.CharField('Apellido materno',max_length=50,blank=True, null=True)
    fecha_nacimiento_desaparecido = models.DateField('Fecha de nacimiento',blank=True, null=True)
    direccion_desaparecido = models.CharField('Dirección',max_length=100,blank=True, null=True)
    observaciones = models.CharField('Observaciones',max_length=250)
    estatus = models.ForeignKey("localizacion_personas.Estatus",verbose_name='Estatus', on_delete=models.CASCADE)
    ultimo_lugar = models.CharField('Último lugar dónde se sabe al desaparecido(a)',max_length=100)
    fecha_desaparicion = models.DateField('Fecha de último contacto')
    telefono_solicitante = models.CharField("Teléfono",max_length=10,validators=[RegexValidator('^(\d{10})$')],blank=True, null=True)
    nombre_solicitante = models.CharField('Nombre',max_length=50)
    apellido_paterno_solicitante = models.CharField('Apellido paterno',max_length=50)
    apellido_materno_solicitante = models.CharField('Apellido materno',max_length=50, blank=True, null=True)
    parentesco = models.CharField('Parentesco',max_length=50)
    empleado = models.ForeignKey("empleados.Empleado",verbose_name='Empleado',on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_desaparecido
    
    class Meta:
        verbose_name = 'Persona desaparecida'
        verbose_name_plural = 'Personas desaparecidas'

class Estatus(models.Model):
    estatus = models.CharField(max_length=30)

    def __str__(self):
        return self.estatus
    class Meta:
        verbose_name = 'Estatus'
        verbose_name_plural = 'Estatus'