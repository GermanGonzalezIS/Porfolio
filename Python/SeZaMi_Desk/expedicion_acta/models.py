from django.db import models
from django.core.validators import RegexValidator

class ExpedicionActa(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    nombre_solicitante = models.CharField("Nombre del solicitante", max_length=100)
    fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
    municipio_registro = models.ForeignKey('catalogos.Municipio',verbose_name="Municipio",on_delete=models.CASCADE, null=True)
    tramite = models.ForeignKey('tramites.Tramite',verbose_name='Trámite',on_delete=models.CASCADE)
