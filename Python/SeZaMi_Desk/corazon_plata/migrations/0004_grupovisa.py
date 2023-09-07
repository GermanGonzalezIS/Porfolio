# Generated by Django 3.2.3 on 2021-08-26 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corazon_plata', '0003_federaciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoVisa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representante', models.CharField(max_length=50, verbose_name='Nombre completo del representante')),
                ('cita_secretaria', models.DateField(verbose_name='Fecha de la cita en la secretaría')),
                ('cita_consulado', models.DateField(verbose_name='Fecha de la cita en el consulado')),
                ('federacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corazon_plata.federaciones', verbose_name='Federación')),
            ],
        ),
    ]