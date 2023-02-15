import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'beauty_shop.settings'
)

app = Celery('beauty_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

