# Generated by Django 2.0.2 on 2018-09-06 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diezmos', '0002_concepto_egreso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingreso',
            name='numero_trans',
            field=models.IntegerField(blank=True, null=True, verbose_name='Numero de Transferencia'),
        ),
    ]