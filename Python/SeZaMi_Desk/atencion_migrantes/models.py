from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class AtencionMigrantes(models.Model):    
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    identificacion_oficial = models.BooleanField("Identificación Oficial", default = False)
    curp_doc = models.BooleanField("CURP",  default = False)
    rfc = models.BooleanField("RFC",  default = False)
    solicitud_gobernador = models.BooleanField("Solicitud al gobernador",  default = False)
    hoja_deportacion = models.BooleanField("Hoja de deportación",  default = False)
    comprobante_domicilio = models.BooleanField("Comprobante de domicilio",  default = False)
    acta_nacimiento = models.BooleanField("Acta de nacimiento",  default = False)
    
    # Foreign keys
    tramite = models.ForeignKey("tramites.Tramite", verbose_name="Trámite", on_delete=models.CASCADE)

