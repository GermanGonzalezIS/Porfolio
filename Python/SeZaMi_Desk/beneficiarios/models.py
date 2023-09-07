from django.db import models
from django.core.validators import RegexValidator

class BeneficiarioDireccion(models.Model):
    tipo_vialidad = models.ForeignKey("catalogos.TipoVialidad", verbose_name="Tipo de vialidad", on_delete=models.CASCADE)
    nombre_vialidad = models.CharField("Vialidad", max_length=50)
    numero_exterior = models.PositiveIntegerField("Número exterior")
    numero_interior = models.PositiveIntegerField("Número interior", null = True, blank = True)
    # Quitar los defaults
    municipio = models.ForeignKey("catalogos.Municipio", verbose_name="Municipio", on_delete=models.CASCADE, default="")
    localidad = models.ForeignKey("catalogos.Localidad", verbose_name="Localidad", on_delete=models.CASCADE, default="")
    asentamiento = models.ForeignKey("catalogos.Asentamiento",verbose_name="Asentamiento", on_delete=models.CASCADE, default="")
    entre_vialidades = models.CharField("Entre vialidades", max_length=50, blank = True)
    descripcion_ubicacion = models.TextField("Referencias de la ubicación", blank = True)

class EstudioSocioeconomico(models.Model):
    estudio_socioeconomico = models.BooleanField("Presentó estudio socioeconómico")
    estado_civil = models.ForeignKey("catalogos.EstadoCivil", verbose_name="Estado civíl", on_delete=models.CASCADE)
    jefe_familia = models.BooleanField("Es jefe de familia")
    ocupacion = models.ForeignKey("catalogos.Ocupacion", verbose_name="Ocupación", on_delete=models.CASCADE)
    ingreso_mensual = models.ForeignKey("catalogos.IngresoMensual", verbose_name="Ingreso mensual", on_delete=models.CASCADE)
    integrantes_familia = models.PositiveIntegerField("Número de integrantes de la familia")
    dependientes_economicos = models.PositiveIntegerField("Número de dependientes económicos")
    vivienda = models.ForeignKey("catalogos.Vivienda", verbose_name="Vivienda", on_delete=models.CASCADE)
    numero_habitantes_vivienda = models.PositiveIntegerField("Número de habitantes en la vivienda")
    vivienda_electricidad = models.BooleanField("Electricidad", default = False)
    vivienda_agua = models.BooleanField("Agua corriente", default = False)
    vivienda_drenaje = models.BooleanField("Drenaje", default = False)
    vivienda_gas = models.BooleanField("Gas", default = False)
    vivienda_telefono = models.BooleanField("Teléfono", default = False)
    vivienda_internet = models.BooleanField("Internet", default = False)
    nivel_estudios = models.ForeignKey("catalogos.NivelEstudios", verbose_name="Nivel de estudios", on_delete=models.CASCADE)
    tipo_seguridad_social = models.ForeignKey("catalogos.TipoSeguridadSocial", verbose_name="Tipo de seguridad social", on_delete=models.CASCADE)
    discapacidad = models.ForeignKey("catalogos.Discapacidad", verbose_name="Discapacidad", on_delete=models.CASCADE)
    grupo_vulnerable = models.ForeignKey("catalogos.GrupoVulnerable", verbose_name="Grupo vulnerable", on_delete=models.CASCADE)

# Create your models here.
# Test commit
class Beneficiario(models.Model):
    # DATOS PERSONALES
    curp = models.CharField("CURP", primary_key = True, max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    primer_apellido = models.CharField("Primer apellido", max_length=50)
    segundo_apellido = models.CharField("Segundo apellido", max_length=50)
    nombre = models.CharField("Nombre(s)", max_length=50)
    identificacion = models.ForeignKey("catalogos.IdentificacionOficial", verbose_name="Identificación Oficial", on_delete=models.CASCADE)
    beneficiario_colectivo = models.BooleanField("Es beneficiario colectivo", default = False)
    direccion = models.ForeignKey("beneficiarios.BeneficiarioDireccion", verbose_name="Dirección", on_delete=models.CASCADE, null = True)
    estudio_socioeconomico = models.ForeignKey("beneficiarios.EstudioSocioeconomico",verbose_name="Estudio Socioeconómico",on_delete=models.CASCADE, null=True)