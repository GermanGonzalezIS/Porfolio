# Generated by Django 3.2.3 on 2021-06-23 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0002_auto_20210614_2038'),
        ('beneficiarios', '0004_auto_20210623_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiariodireccion',
            name='asentamiento',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.asentamiento', verbose_name='Asentamiento'),
        ),
        migrations.AlterField(
            model_name='beneficiariodireccion',
            name='localidad',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.localidad', verbose_name='Localidad'),
        ),
    ]