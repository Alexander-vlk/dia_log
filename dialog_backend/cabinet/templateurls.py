from django.urls import path

from cabinet.templateviews import (
    index,
    cabinet,
    edit_profile,
    get_daily_log_fill_status,
    get_weekly_log_fill_status,
)

urlpatterns = [
    path('', index, name='index'),
    path('cabinet/', cabinet, name='cabinet'),

    path('cabinet/update', edit_profile, name='cabinet_update'),

    path('cabinet/daily_log/filled/', get_daily_log_fill_status, name='get_daily_log_fill_status'),

    path('cabinet/weekly_log/fill/', get_weekly_log_fill_status, name='get_weekly_log_fill_status'),
]