from django.db import models
from django.core.validators import RegexValidator

class MandamientosJudiciales(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    acta_nac_original = models.BooleanField("Acta de Nacimiento Original",default=False) 
    curp_act = models.BooleanField("CURP Actualizada",default=False) 
    comprobante_domicilio = models.BooleanField("Comprobante domicilio",default=False) 
    pasaporte_vigente = models.BooleanField("Pasaporte vigente",default=False) 
    matricula_consular = models.BooleanField("Matrícula Consular",default=False) 
    pago_en_caja_fiscalia = models.BooleanField("Pago que se realiza en caja de fiscalía",default=False) 
    fotografia= models.BooleanField("Fotografía tamaño infantil blanco y negro con fondo blanco",default=False) 
    ine_familiar = models.BooleanField("INE del familiar directo que va a tramitar el documento",default=False) 
    tramite = models.ForeignKey('tramites.Tramite',verbose_name='Trámite',on_delete=models.CASCADE)
