from django.urls import path

from data_tracking.templateviews import (
    daily_log,
    DailyLogListView,
    monthly_log_list,
    weekly_log,
    WeeklyLogListView,
)

urlpatterns = [

    path('daily_log', daily_log, name='daily_log'),
    path('weekly_log', weekly_log, name='weekly_log'),
    path('daily_log_list', DailyLogListView.as_view(), name='daily_log_list'),
    path('weekly_log_list', WeeklyLogListView.as_view(), name='weekly_log_list'),
    path('monthly_logs/<int:monthly_log_id>', monthly_log_list, name='monthly_log'),
]
