from django.db import models
from django.core.validators import RegexValidator

class CorreccionActa(models.Model):
    curp = models.CharField("CURP", default = "", max_length=18, validators=[RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\d)')])
    acta_a_corregir = models.BooleanField("Acta a corregir",default=False)   
    documentos_comprobantes = models.BooleanField("Documentos que comprueben lo solicitado",default=False)
    testimonial = models.BooleanField("Testimonial de 2 personas",default=False)  
    solicitud_firmado = models.BooleanField("Solicitud firmada",default=False)    
    original_copias = models.BooleanField("Original y 2 Copias",default=False)   
    tramite = models.ForeignKey('tramites.Tramite',verbose_name='Trámite',on_delete=models.CASCADE)