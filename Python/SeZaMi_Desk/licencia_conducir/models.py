from django.db import models
from django.core.validators import RegexValidator

class LicenciaConducir(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    acta_nacimiento = models.BooleanField("Acta de Nacimiento",default=False)
    comprobante_dom_eeuu = models.BooleanField("Comprobante de domicilio en Estados Unidos",default=False)
    referencia_dom_zac = models.BooleanField("Domicilio de referencia en el Estado de Zacatecas",default=False)
    fotografia = models.BooleanField("Fotografía",default=False)
    tipo_sangre = models.CharField("Tipo de Sangre", max_length=3, validators=[RegexValidator('^(A|B|AB|O)[-+]$')])
    identificacion_oficial = models.BooleanField("Identificación oficial",default=False) 
    tramite = models.ForeignKey('tramites.Tramite',verbose_name='Trámite',on_delete=models.CASCADE)
