# django_celery/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg_notifier_assignment.settings")
app = Celery("tg_notifier_assignment")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'tg_notification_check_periodic_task': {
        'task': 'tg_notification_periodic_check_task',
        'schedule': 30.0
    },
}