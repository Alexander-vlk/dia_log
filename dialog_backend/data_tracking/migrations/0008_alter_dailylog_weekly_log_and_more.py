# Generated by Django 5.1.5 on 2025-04-05 08:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_tracking', '0007_weeklylog_monthly_log'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailylog',
            name='weekly_log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_tracking.weeklylog', verbose_name='Недельный отчет'),
        ),
        migrations.AlterUniqueTogether(
            name='dailylog',
            unique_together={('user', 'date')},
        ),
    ]
