# Generated by Django 3.2.3 on 2021-08-27 04:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tramites', '0005_auto_20210824_2332'),
        ('catalogos', '0002_auto_20210614_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpedicionActa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curp', models.CharField(default='', max_length=18, validators=[django.core.validators.RegexValidator('([A-Z]{4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[A-Z]{3}[0-9A-Z]\\d)')], verbose_name='CURP')),
                ('nombre_solicitante', models.CharField(max_length=100, verbose_name='Nombre del solicitante')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('municipio_registro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogos.municipio', verbose_name='Municipio')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tramites.tramite', verbose_name='Trámite')),
            ],
        ),
    ]
