# Generated by Django 2.0.2 on 2018-10-19 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0006_auto_20180902_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='cedula',
            field=models.CharField(max_length=9, unique=True, verbose_name='Cedula'),
        ),
    ]
