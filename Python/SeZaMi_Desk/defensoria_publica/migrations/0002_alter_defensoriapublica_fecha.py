# Generated by Django 3.2.3 on 2021-08-27 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defensoria_publica', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defensoriapublica',
            name='fecha',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha de trámite'),
        ),
    ]
