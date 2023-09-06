# Generated by Django 3.2.8 on 2021-12-05 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_publicaciones', '0001_initial'),
        ('publicaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='publicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='publicaciones.publicacion', verbose_name='Publicación'),
        ),
    ]