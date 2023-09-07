from django.db import models
from django.core.validators import RegexValidator


class DefensoriaPublica(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    tramite_realizar = models.CharField("Trámite a Realizar", max_length=80, default="")
    localidad = models.ForeignKey("catalogos.Localidad",verbose_name="Localidad", on_delete=models.CASCADE, null=True)
    num_telefonico = models.CharField(verbose_name="Número de teléfono", validators=[RegexValidator('\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$')], max_length=15,null=True)
    email = models.EmailField("Correo electrónico", default="")
    tramite = models.ForeignKey('tramites.Tramite',verbose_name='Trámite',on_delete=models.CASCADE)