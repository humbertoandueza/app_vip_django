# Generated by Django 2.0.2 on 2018-09-02 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_remove_persona_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='rol',
            field=models.CharField(choices=[('Miembro', 'Miembro'), ('Lider', 'Lider'), ('Asistente', 'Asistente')], default=1, max_length=40),
            preserve_default=False,
        ),
    ]
