# Generated by Django 3.2.3 on 2021-09-08 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corazon_plata', '0006_auto_20210827_0322'),
    ]

    operations = [
        migrations.AddField(
            model_name='corazonplata',
            name='datos_completos',
            field=models.BooleanField(default=False, verbose_name='Se entregaron todos los datos'),
        ),
    ]