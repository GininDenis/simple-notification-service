import requests

from celery import Celery

from apps.notifications.models import Subscription

app = Celery('sns')
