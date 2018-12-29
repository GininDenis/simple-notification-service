import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('sns', broker='redis://')
app.autodiscover_tasks()
