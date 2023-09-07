from django.db import models
from django.core.validators import RegexValidator

class IdentificacionOficial(models.Model):
    identificacion = models.CharField('Tipo de identificación', max_length=30)

    def __str__(self):
        return self.identificacion

class TipoVialidad(models.Model):
    vialidad = models.CharField('Tipo de vialidad', max_length=20)

    def __str__(self):
        return self.vialidad

    class Meta:
        verbose_name = 'Tipo de vialidad'
        verbose_name_plural = 'Tipos de vialidades'

class EstadoCivil(models.Model):
    estado_civil = models.CharField('Estado Civil',max_length=20)

    def __str__(self):
        return self.estado_civil

class Ocupacion(models.Model):
    ocupacion = models.CharField('Tipo de ocupación', max_length=30)

    def __str__(self):
        return self.ocupacion

class IngresoMensual(models.Model):
    descripcion = models.CharField('Descripción del ingreso', max_length=80)

    def __str__(self):
        return self.descripcion

class Vivienda(models.Model):
    vivienda = models.CharField('Tipo de vivienda', max_length=20)
    
    def __str__(self):
        return self.vivienda

    class Meta:
        verbose_name = 'Vivienda'
        verbose_name_plural = 'Viviendas'

class NivelEstudios(models.Model):
    nivel_estudio = models.CharField('Nivel de estudios', max_length=20)
    
    def __str__(self):
        return self.nivel_estudio

    class Meta:
        verbose_name = 'Nivel de estudio'
        verbose_name_plural = 'Niveles de estudio'

class TipoSeguridadSocial(models.Model):
    seguridad_social = models.CharField('Seguridad social', max_length=20)
    def __str__(self):
        return self.seguridad_social

class Discapacidad(models.Model):
    discapacidad = models.CharField('Tipo de discapacidad', max_length=60)

    def __str__(self):
        return self.discapacidad

    class Meta:
        verbose_name = 'Discapacidad'
        verbose_name_plural = 'Discapacidades'
        
class GrupoVulnerable(models.Model):
    grupo_vulnerable = models.CharField('Grupo vulnerable', max_length=80)

    def __str__(self):
        return self.grupo_vulnerable
        
    class Meta:
        verbose_name = 'Grupo vulnerable'
        verbose_name_plural = 'Grupos vulnerables'

class Municipio(models.Model):
    id = models.PositiveIntegerField('ID',primary_key=True)
    municipio = models.CharField('Municipio', max_length=35)

    def __str__(self):
        return self.municipio
        
    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

class Localidad(models.Model):
    id = models.PositiveIntegerField('ID',primary_key=True)
    localidad = models.CharField('Localidad',max_length=100)
    municipio = models.ForeignKey('catalogos.Municipio',verbose_name='Municipio',on_delete=models.CASCADE)
    ambito = models.ForeignKey("catalogos.AmbitoLocalidad", verbose_name='Ámbito', on_delete=models.CASCADE,default=1) 

    def __str__(self):
        return self.localidad

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
    
class Asentamiento(models.Model):
    id = models.CharField('ID',primary_key=True,max_length=13,validators=[RegexValidator(r'^[1-9]\d*$')])
    asentamiento = models.CharField('Asentamiento',max_length=60)
    tipo_asentamiento = models.PositiveIntegerField('Tipo de asentamiento')
    localidad = models.ForeignKey('catalogos.Localidad',verbose_name='Localidad',on_delete=models.CASCADE)

    def __str__(self):
        return self.asentamiento

    class Meta:
        verbose_name = 'Asentamiento'
        verbose_name_plural = 'Asentamientos'

class AmbitoLocalidad(models.Model):
    ambito = models.CharField('Ámbito de localidad', max_length=10)

    def __str__(self):
        return self.ambito