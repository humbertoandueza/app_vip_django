# Generated by Django 2.0.2 on 2018-10-08 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0006_actividades_suspended'),
    ]

    operations = [
        migrations.AddField(
            model_name='iglesia',
            name='email',
            field=models.EmailField(default=1, max_length=254, verbose_name='Correo'),
            preserve_default=False,
        ),
    ]