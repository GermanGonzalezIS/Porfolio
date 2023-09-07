from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class Pasaporte(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    acta = models.BooleanField("Acta Original", default = False)
    seguro_social = models.BooleanField("Seguro Social", default = False)
    identificacion_padres = models.BooleanField("Identificación de los padres", default = False)
    nombre_contacto_usa = models.CharField("Nombre de la persona a visitar",max_length=70, null=True)
    direccion_usa = models.CharField("Dirección de Estados Unidos", max_length=70, null=True)
    tel_contacto_usa = models.CharField(verbose_name="Teléfono contacto en Estados Unidos", validators=[RegexValidator('\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$')], max_length=15,null=True)
    correo = models.CharField('Correo electrónico',max_length=50,null=True)
    tramite = models.ForeignKey("tramites.Tramite", verbose_name="Trámite", on_delete=models.CASCADE)

class Seguro(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    years_work = models.BooleanField("Años trabajo", default = False)
    years = models.BooleanField("Años cumplidos", default = False)
    numero_seguro_social = models.BooleanField("Número de seguro social", default = False)
    tramite = models.ForeignKey("tramites.Tramite", verbose_name="Trámite", on_delete=models.CASCADE)