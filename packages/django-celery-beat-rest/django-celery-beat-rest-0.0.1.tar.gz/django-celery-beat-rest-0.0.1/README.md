django-celery-beat RESTful API
==============================

RESTful API for django-celery-beat.

# Usage

Add `'celery_beat_rest'` in your project's `settings.py`:

```
INSTALLED_APPS = [
    'celery_beat_rest',
]
```

Include `celery_beat_rest.urls` in project's `urls.py`:

```
urlpatterns = [
    path('celery/beat/', include('celery_beat_rest.urls'))
]
```
