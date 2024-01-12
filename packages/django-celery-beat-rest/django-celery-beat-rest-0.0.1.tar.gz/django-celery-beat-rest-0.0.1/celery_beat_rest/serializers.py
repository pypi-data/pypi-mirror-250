from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField
from django_celery_beat.models import (
    ClockedSchedule, SolarSchedule, SOLAR_SCHEDULES, CrontabSchedule, IntervalSchedule, PeriodicTask
)


class ClockedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = '__all__'


class SolarScheduleSerializer(serializers.ModelSerializer):
    event = serializers.ChoiceField(choices=SOLAR_SCHEDULES)

    class Meta:
        model = SolarSchedule
        fields = '__all__'


class CrontabScheduleSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField(use_pytz=False)
    human_readable = serializers.ReadOnlyField()

    class Meta:
        model = CrontabSchedule
        fields = '__all__'


class IntervalScheduleSerializer(serializers.ModelSerializer):
    period = serializers.ChoiceField(choices=IntervalSchedule.PERIOD_CHOICES)

    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'


class PeriodicTaskListSerializer(serializers.ModelSerializer):
    scheduler = serializers.ReadOnlyField(source='scheduler.__str__')

    class Meta:
        model = PeriodicTask
        fields = ['name', 'enabled', 'scheduler', 'interval', 'start_time', 'last_run_at', 'one_off']
