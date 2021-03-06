from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from backend import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'add-every-2-hour': {
        'task': 'event.tasks.task_run_beat',
        # 'schedule': 120.0,
        'schedule': crontab(hour=1),
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
