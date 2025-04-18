from django.urls import path

from data_tracking.views.private import (
    AverageGlucoseDataAPIView,
    BodyTemperatureAPIView,
    CaloriesAPIView,
    GlucoseAPIView,
    PressureAPIView,
    WeeklyLogAPIView,
)

urlpatterns = [
    path('average-glucose/', AverageGlucoseDataAPIView.as_view(), name='average-glucose'),
    path('body-temperature/', BodyTemperatureAPIView.as_view(), name='body_temperature'),
    path('calories/', CaloriesAPIView.as_view(), name='calories'),
    path('glucose/', GlucoseAPIView.as_view(), name='glucose'),
    path('pressure/', PressureAPIView.as_view(), name='pressure'),

    path('weekly-log/', WeeklyLogAPIView.as_view(), name='weekly_log'),
]
