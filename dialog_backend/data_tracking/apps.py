from django.apps import AppConfig


class DataTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_tracking'
    verbose_name = 'Отслеживание состояния'
