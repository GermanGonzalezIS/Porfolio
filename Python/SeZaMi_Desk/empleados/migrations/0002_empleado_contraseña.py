# Generated by Django 3.2.3 on 2021-06-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='contraseña',
            field=models.CharField(default=None, max_length=50, verbose_name='Contraseña'),
        ),
    ]
