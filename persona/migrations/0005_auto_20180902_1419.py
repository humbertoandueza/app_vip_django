# Generated by Django 2.0.2 on 2018-09-02 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0004_auto_20180902_1416'),
    ]

    operations = [
        migrations.RenameField(
            model_name='persona',
            old_name='rol',
            new_name='roles',
        ),
    ]
