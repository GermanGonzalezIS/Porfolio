# Generated by Django 3.2.3 on 2021-06-14 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asentamiento',
            old_name='nombre',
            new_name='asentamiento',
        ),
        migrations.RenameField(
            model_name='localidad',
            old_name='nombre',
            new_name='localidad',
        ),
        migrations.RenameField(
            model_name='municipio',
            old_name='nombre',
            new_name='municipio',
        ),
    ]
