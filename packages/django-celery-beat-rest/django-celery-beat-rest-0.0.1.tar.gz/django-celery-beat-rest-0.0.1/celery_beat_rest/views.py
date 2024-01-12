from rest_framework import viewsets, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_celery_beat.admin import TaskSelectWidget
from django_celery_beat.models import (
    ClockedSchedule, SolarSchedule, SOLAR_SCHEDULES, CrontabSchedule, IntervalSchedule, PeriodicTask
)
from .serializers import (
    ClockedScheduleSerializer, SolarScheduleSerializer, CrontabScheduleSerializer, IntervalScheduleSerializer,
    PeriodicTaskSerializer, PeriodicTaskListSerializer
)
from .filters import (
    ClockedScheduleFilter, SolarScheduleFilter, CrontabScheduleFilter, IntervalScheduleFilter, PeriodicTaskFilter
)


class ClockedScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClockedSchedule.objects.all()
    serializer_class = ClockedScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = ClockedScheduleFilter
    ordering_fields = ['id']


class SolarScheduleViewSet(viewsets.ModelViewSet):
    queryset = SolarSchedule.objects.all()
    serializer_class = SolarScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = SolarScheduleFilter
    ordering_fields = ['id']

    @action(detail=False, methods=['get'])
    def events(self, request, pk=None):
        return Response(SOLAR_SCHEDULES, status=status.HTTP_200_OK)


class CrontabScheduleViewSet(viewsets.ModelViewSet):
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = CrontabScheduleFilter
    ordering_fields = ['id']

    @action(detail=False, methods=['get'])
    def timezones(self, request, pk=None):
        return Response([(v, v) for _, v in CrontabSchedule._meta.get_field('timezone').choices],
                        status=status.HTTP_200_OK)


class IntervalScheduleViewSet(viewsets.ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = IntervalScheduleFilter
    ordering_fields = ['id']

    @action(detail=False, methods=['get'])
    def periods(self, request, pk=None):
        return Response(IntervalSchedule.PERIOD_CHOICES, status=status.HTTP_200_OK)


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = PeriodicTaskFilter
    ordering_fields = ['id']

    def get_serializer_class(self):
        if self.action == 'list':
            return PeriodicTaskListSerializer
        else:
            return PeriodicTaskSerializer

    @action(detail=False, methods=['get'])
    def tasks(self, request, pk=None):
        return Response(TaskSelectWidget().choices[1:], status=status.HTTP_200_OK)
