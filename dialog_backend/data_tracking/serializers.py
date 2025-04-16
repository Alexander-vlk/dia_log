from datetime import date, timedelta

from django.utils import timezone
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from data_tracking.models import (
    BodyTemperature,
    DailyLog,
    Glucose,
    MonthlyLog,
    Pressure,
    WeeklyLog,
)


class MonthlyLogSerializer(serializers.ModelSerializer):
    """Сериализатор модели MonthlyLog"""

    class Meta:
        model = MonthlyLog
        fields = (
            'hemoglobin',
            'cholesterol',
            'lipid_profile',
            'microalbuminuria',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            return MonthlyLog.objects.create(user=user, **validated_data)


class WeeklyLogSerializer(serializers.ModelSerializer):
    """Сериализатор модели WeeklyLog"""

    class Meta:
        model = WeeklyLog
        fields = (
            'weight',
            'bmi',
            'ketones',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        week_start = date.today()
        week_end = week_start + timedelta(days=7)
        if user.is_authenticated:
            return WeeklyLog.objects.create(user=user, date=week_start, **validated_data)

        return WeeklyLog.objects.create(week_start=week_start, week_end=week_end,**validated_data)


class DailyLogSerializer(serializers.ModelSerializer):
    """Сериализатор модели DailyLog"""

    class Meta:
        model = DailyLog
        fields = (
            'calories_count',
            'proteins_count',
            'fats_count',
            'carbs_count',
            'general_health',
            'physical_activity',
            'additional_info',
        )

    def validate_date(self, value):
        user = self.context['request'].user
        if user.is_authenticated and DailyLog.objects.filter(user=user, date=value).exists():
            raise serializers.ValidationError('Дневной отчет для этого дня уже существует')
        if value > date.today():
            raise serializers.ValidationError('Нельзя создать дневной отчет для еще не наступившего дня')

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            return DailyLog.objects.create(
                user=user,
                date=date.today(),
                **validated_data,
            )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Return data example',
            description='Return temperature and creation date (format: HH:MM)',
            summary='Data for plots',
            value={
                'created_at': '10:00',
                'temperature': 36.6,
            },
        ),
    ],
    many=True,
)
class BodyTemperatureSerializer(serializers.ModelSerializer):
    """Сериализатор модели BodyTemperature"""

    created_at = serializers.DateTimeField(format='%H:%M', required=False, read_only=True)

    class Meta:
        model = BodyTemperature
        fields = (
            'created_at',
            'temperature',
        )

    def create(self, validated_data):
        user = self.context.get('user')

        if not user:
            return BodyTemperature.objects.create(
                **validated_data,
            )

        daily_log = DailyLog.objects.filter(user=user, date=timezone.now()).first()
        if not daily_log:
            BodyTemperature.objects.create(
                user=user,
                **validated_data,
            )

        return BodyTemperature.objects.create(
            user=user,
            daily_log=daily_log,
            **validated_data,
        )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Return data example',
            description='Two fields: creation date and glucose level, need for plot creation',
            summary='Data for plots',
            value={
                'created_at': '23:00',
                'level': 3.4,
            },
        ),
    ],
    many=True,
)
class GlucoseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Glucose"""

    created_at = serializers.DateTimeField(format='%H:%M', required=False, read_only=True)

    class Meta:
        model = Glucose
        fields = (
            'created_at',
            'level',
        )

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            return Glucose.objects.create(**validated_data)

        daily_log = DailyLog.objects.filter(user=user, date=timezone.now()).first()
        if not daily_log:
            return Glucose.objects.create(user=user, **validated_data)

        return Glucose.objects.create(user=user, daily_log=daily_log, **validated_data)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Return data example',
            description='Two fields: creation date, systolic and diastolic pressure',
            summary='Data for plot',
            value={
                'created_at': '23:00',
                'systolic': 120,
                'diastolic': 80,
            }
        )
    ],
    many=True,
)
class PressureSerializer(serializers.ModelSerializer):
    """Сериализатор модели Pressure"""

    created_at = serializers.DateTimeField(format='%H:%M', required=False, read_only=True)

    class Meta:
        model = Pressure
        fields = (
            'created_at',
            'systolic',
            'diastolic',
        )

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            return Pressure.objects.create(**validated_data)

        daily_log = DailyLog.objects.filter(user=user, date=timezone.now()).first()
        if not daily_log:
            return Pressure.objects.create(user=user, **validated_data)

        return Pressure.objects.create(user=user, daily_log=daily_log, **validated_data)
