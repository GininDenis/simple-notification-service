import requests
import json
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.models import Site
from urllib.parse import urljoin

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.notifications.models import Subscription
from apps.notifications.tokens import subscription_activation_token
from conf.celery_app import app


def get_endpoint(instance):
    if settings.SUBSCRIPTION_ENDPOINT_DEBUG:
        assert settings.TEST_ENDPOINT_URL, \
                'You have to define TEST_ENDPOINT_URL in settings when SUBSCRIPTION_ENDPOINT_DEBUG is True'
        return settings.TEST_ENDPOINT_URL
    return instance.endpoint

def create_message(object_id):
    instance = Subscription.objects.get(id=object_id)
    message = {
        'type': 'SubscriptionConfirmation',
        'subscription_url': '',
        'subscription_id': instance.pk,
        'token': instance.token,
        'message': 'You have to confirm subscription, please follow the ‘subscription_url’ link'
    }
    uid = urlsafe_base64_encode(force_bytes(instance.pk)).decode('utf-8')
    token = subscription_activation_token.make_token(instance)
    activate_url = reverse('notifications:subscription-confirm',
                           kwargs={'token': token, 'uid': uid})
    site = Site.objects.get_current()
    message['subscription_url'] = urljoin(site.domain, activate_url)
    return instance, message


@app.task
def send_subscription_confirmation(object_id):
    instance, message = create_message(object_id)
    instance.attempts_count += 1
    rs = requests.post(get_endpoint(instance), data=message)
    if rs.status_code != 200:
        instance.error_msg = rs.text
    else:
        instance.error_msg = None
    instance.save(update_fields=['error_msg', 'attempts_count'])
