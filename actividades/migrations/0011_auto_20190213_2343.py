# Generated by Django 2.0.2 on 2019-02-14 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0010_auto_20190213_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Imagen',
        ),
        migrations.AlterField(
            model_name='album',
            name='imagen',
            field=models.ManyToManyField(to='actividades.Photo'),
        ),
    ]