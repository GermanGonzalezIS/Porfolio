# Generated by Django 3.2.3 on 2021-08-27 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expedicion_acta', '0004_alter_expedicionacta_fecha_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expedicionacta',
            name='fecha_nacimiento',
            field=models.DateField(null=True, verbose_name='Fecha de nacimiento'),
        ),
    ]
