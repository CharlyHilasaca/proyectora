# Generated by Django 5.1.6 on 2025-02-21 03:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_dev', '0003_alter_dev_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dev',
            name='roles',
            field=models.ForeignKey(default='default_role', on_delete=django.db.models.deletion.SET_DEFAULT, to='rep_dev.roles'),
        ),
    ]
