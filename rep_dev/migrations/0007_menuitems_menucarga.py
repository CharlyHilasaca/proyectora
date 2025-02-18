# Generated by Django 5.1.6 on 2025-02-17 04:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_dev', '0006_delete_menucarga_delete_menuitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_opcion', models.CharField(max_length=100, unique=True)),
                ('data', models.CharField(max_length=100)),
                ('class_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MenuCarga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rep_dev.dev')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rep_dev.menuitems')),
            ],
        ),
    ]
