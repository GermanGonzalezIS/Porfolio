# Generated by Django 3.2.3 on 2021-08-26 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandamientos_judiciales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandamientosjudiciales',
            name='pago_en_caja_fiscalia',
            field=models.BooleanField(default=False, verbose_name='Pago que se realiza en caja de fiscalía'),
        ),
    ]
