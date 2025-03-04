# Generated by Django 5.1.6 on 2025-02-23 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_dev', '0006_opcion_descripcion_delete_devdescripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dev',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='dev',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dev',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
