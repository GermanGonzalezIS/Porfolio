# Generated by Django 3.2.3 on 2021-08-26 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corazon_plata', '0004_grupovisa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupovisa',
            name='cita_consulado',
            field=models.DateField(null=True, verbose_name='Fecha de la cita en el consulado'),
        ),
        migrations.AlterField(
            model_name='grupovisa',
            name='cita_secretaria',
            field=models.DateField(null=True, verbose_name='Fecha de la cita en la secretaría'),
        ),
    ]