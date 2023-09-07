# Generated by Django 3.2.3 on 2021-08-27 10:05

from django.db import migrations, models
import django.db.models.deletion
import doble_nacionalidad.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tramites', '0005_auto_20210824_2332'),
        ('empleados', '0003_rename_contraseña_empleado_contra'),
    ]

    operations = [
        migrations.CreateModel(
            name='DobleNacionalidad',
            fields=[
                ('folio', models.IntegerField(default=doble_nacionalidad.models.autoincremento_folio, primary_key=True, serialize=False, verbose_name='folio')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido_paterno', models.CharField(max_length=50, verbose_name='Apellido paterno')),
                ('apellido_materno', models.CharField(blank=True, max_length=50, null=True, verbose_name='Apellido materno')),
                ('acta_nacimiento_original', models.BooleanField(default=False, verbose_name='Acta de Nacimiento Original')),
                ('actas_apostilladas', models.BooleanField(default=False, verbose_name='Actas apostilladas')),
                ('comprobante_domicilio', models.BooleanField(default=False, verbose_name='Comprobante de domicilio')),
                ('identificacion_oficial', models.BooleanField(default=False, verbose_name='Identificación Oficial Padres')),
                ('original_copias', models.BooleanField(default=False, verbose_name='Original y 2 Copias tama')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empleados.empleado', verbose_name='Empleado')),
                ('tramite_estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tramites.nombretramites', verbose_name='Estado trámite')),
            ],
        ),
    ]