from django.db import models
from django.core.validators import RegexValidator

class Apostilla(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    acta_americana = models.BooleanField('Acta americana',default=False)
    acta_mexicana = models.BooleanField('Acta mexicana',default=False)
    identificacion_padres = models.BooleanField('Identificación oficial de ambos padres',default=False)
    curp_doc = models.BooleanField('CURP',default=False)
    comprobante_domicilio = models.BooleanField('Comprobante de domicilio',default=False)
    rfc = models.BooleanField('RFC',default=False)
    tramite = models.ForeignKey('tramites.Tramite',verbose_name='Trámite',on_delete=models.CASCADE)