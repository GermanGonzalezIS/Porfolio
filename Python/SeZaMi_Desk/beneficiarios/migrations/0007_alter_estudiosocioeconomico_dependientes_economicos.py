# Generated by Django 3.2.3 on 2021-06-29 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiarios', '0006_auto_20210623_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiosocioeconomico',
            name='dependientes_economicos',
            field=models.PositiveIntegerField(verbose_name='Número de dependientes económicos'),
        ),
    ]