# Generated by Django 3.2.3 on 2021-06-23 17:30

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0002_auto_20210614_2038'),
        ('beneficiarios', '0003_alter_beneficiariodireccion_descripcion_ubicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiariodireccion',
            name='localidad',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='municipio', chained_model_field='municipio', default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.localidad', verbose_name='Localidad'),
        ),
        migrations.AddField(
            model_name='beneficiariodireccion',
            name='municipio',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.municipio', verbose_name='Municipio'),
        ),
        migrations.AlterField(
            model_name='beneficiariodireccion',
            name='asentamiento',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='localidad', chained_model_field='localidad', default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogos.asentamiento', verbose_name='Asentamiento'),
        ),
    ]
