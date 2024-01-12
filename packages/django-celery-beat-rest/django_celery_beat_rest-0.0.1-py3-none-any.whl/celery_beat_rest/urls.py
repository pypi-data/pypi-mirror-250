from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'clockedschedules', views.ClockedScheduleViewSet)
router.register(r'solarschedules', views.SolarScheduleViewSet)
router.register(r'crontabschedules', views.CrontabScheduleViewSet)
router.register(r'intervalschedules', views.IntervalScheduleViewSet)
router.register(r'periodictasks', views.PeriodicTaskViewSet)


urlpatterns = [
    path('', include(router.urls))
]
