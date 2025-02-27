# Generated by Django 5.1.5 on 2025-02-09 11:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0004_alter_userprofile_diabetes_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='diabetes_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('1 типа', '1'), ('2 типа', '2'), ('MODY-диабет', 'MODY'), ('Гестационный диабет', 'gestational')], max_length=20), blank=True, default=list, size=None, verbose_name='Тип диабета'),
        ),
    ]
