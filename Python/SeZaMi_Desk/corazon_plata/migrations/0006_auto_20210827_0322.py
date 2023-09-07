# Generated by Django 3.2.3 on 2021-08-27 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corazon_plata', '0005_auto_20210826_0633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corazonplata',
            name='copia_cheque',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='copia_ine_representante',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='curp_representante',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='emitio_factura',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='es_organizacion',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='firmo_recibo',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='solicitud_apoyo',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='tiene_cuenta_bancaria',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='titulo_propiedad',
        ),
        migrations.RemoveField(
            model_name='corazonplata',
            name='tramite',
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='certificado_medico',
            field=models.BooleanField(default=False, verbose_name='Certificado médico'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='credencial',
            field=models.BooleanField(default=False, verbose_name='Credencial para votar'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='curp',
            field=models.BooleanField(default=False, verbose_name='CURP'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='grupo_visa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='corazon_plata.grupovisa', verbose_name='Grupo de corazón de plata'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='no_antecedentes',
            field=models.BooleanField(default=False, verbose_name='No antecedentes migratorios'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='nombre_ahijado',
            field=models.CharField(max_length=50, null=True, verbose_name='Nombre completo del ahijado'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='nombre_padrino',
            field=models.CharField(max_length=50, null=True, verbose_name='Nombre completo del ahijado'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='padrino',
            field=models.BooleanField(default=False, verbose_name='Familiar migrante perteneciente a una organización'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='pasaporte',
            field=models.BooleanField(default=False, verbose_name='Pasaporte vigente'),
        ),
        migrations.AddField(
            model_name='corazonplata',
            name='persona_zacatecana',
            field=models.BooleanField(default=False, verbose_name='Es persona zacatecana o residente'),
        ),
    ]