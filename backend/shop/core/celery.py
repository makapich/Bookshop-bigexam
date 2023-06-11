import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'sync-books': {
        'task': 'shop.tasks.books_sync',
        'schedule': crontab(minute='*/2'),
    },
    'sync-order-statuses': {
        'task': 'shop.tasks.orders_sync',
        'schedule': crontab(minute='*/1'),
    }
}
