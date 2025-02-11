# Generated by Django 5.1.5 on 2025-02-11 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_tracking', '0006_alter_monthlylog_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklylog',
            name='monthly_log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_tracking.monthlylog', verbose_name='Ежемесячный отчет'),
        ),
    ]
