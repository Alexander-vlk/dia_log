from django.urls import path

from data_tracking.templateviews import (
    daily_log,
    DailyLogListView,
    weekly_log,
)

urlpatterns = [

    path('daily_log', daily_log, name='daily_log'),
    path('weekly_log', weekly_log, name='weekly_log'),
    path('daily_log_list', DailyLogListView.as_view(), name='daily_log_list'),
]
