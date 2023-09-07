from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class CorazonPlata(models.Model):
    credencial = models.BooleanField("Credencial para votar", default = False)
    pasaporte = models.BooleanField("Pasaporte vigente", default=False)
    curp = models.BooleanField("CURP", default=False)
    persona_zacatecana = models.BooleanField("Es persona zacatecana o residente", default=False)
    certificado_medico = models.BooleanField("Certificado médico", default=False)
    padrino = models.BooleanField("Familiar migrante perteneciente a una organización", default=False)
    no_antecedentes = models.BooleanField("No antecedentes migratorios", default=False)
    nombre_ahijado = models.CharField("Nombre del ahijado", max_length=50, null = True)
    ap_paterno_ahijado = models.CharField("Apellido paterno del ahijado", max_length=50, null = True)
    ap_materno_ahijado = models.CharField("Apellido materno del ahijado", max_length=50, null = True)
    nombre_padrino = models.CharField("Nombre completo del ahijado", max_length=50, null = True)
    # Indicador de que se entregaron todos los datos
    datos_completos = models.BooleanField("Se entregaron todos los datos", default=False)
    # Foreign
    grupo_visa = models.ForeignKey("corazon_plata.GrupoVisa", verbose_name="Grupo de corazón de plata", on_delete=models.CASCADE, null=True)

class GrupoVisa(models.Model):
    federacion = models.ForeignKey("corazon_plata.Federaciones", verbose_name="Federación", on_delete=models.CASCADE)
    representante = models.CharField("Nombre completo del representante", max_length=50)
    cita_secretaria = models.DateField("Fecha de la cita en la secretaría", auto_now=False, auto_now_add=False, null=True)
    cita_consulado = models.DateField("Fecha de la cita en el consulado", auto_now=False, auto_now_add=False, null=True)

class Federaciones(models.Model):
    nombre = models.CharField("Nombre de la federación",max_length=60)

     

