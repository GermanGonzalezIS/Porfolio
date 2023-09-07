# Generated by Django 3.2.3 on 2021-08-24 23:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0004_auto_20210625_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='num_telefonico',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('\\+(9[976]\\d|8[987530]\\d|6[987]\\d|5[90]\\d|42\\d|3[875]\\d|2[98654321]\\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\\d{1,14}$')], verbose_name='Número de teléfono'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tramites.club', verbose_name='Club'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='nombre',
            field=models.CharField(max_length=50, null=True, verbose_name='Nombre del grupo'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='representante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tramites.representante', verbose_name='Representante'),
        ),
    ]
