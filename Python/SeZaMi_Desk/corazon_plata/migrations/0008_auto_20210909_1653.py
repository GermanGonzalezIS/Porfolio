# Generated by Django 3.2.3 on 2021-09-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corazon_plata', '0007_corazonplata_datos_completos'),
    ]

    operations = [
        migrations.AddField(
            model_name='corazonplata',
            name='ap_materno_ahijado',
            field=models.CharField(max_length=50, null=True, verbose_name='Apellido materno del ahijado'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='ap_paterno_ahijado',
            field=models.CharField(max_length=50, null=True, verbose_name='Apellido paterno del ahijado'),
        ),
        migrations.AlterField(
            model_name='corazonplata',
            name='nombre_ahijado',
            field=models.CharField(max_length=50, null=True, verbose_name='Nombre del ahijado'),
        ),
    ]
