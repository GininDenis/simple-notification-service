import requests
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.models import Site
from urllib.parse import urljoin

from apps.notifications.models import Subscription
from apps.notifications.tokens import subscription_activation_token
from conf.celery_app import app


@app.task
def send_subscription_confirmation(object_id):

    instance = Subscription.objects.get(id=object_id)
    message = {
        'type': 'SubscriptionConfirmation',
        'subscription_url': '',
        'token': instance.token,
        'message': 'You have to confirm subscription, please follow the ‘subscription_url’ link'
    }

    token = subscription_activation_token.make_token(instance)
    activate_url = reverse('api:subscription-confirm',
                           kwargs={'token': token})
    site = Site.objects.get_current()
    message['subscription_url'] = urljoin(site.domain, activate_url)

    if settings.SUBSCRIPTION_ENDPOINT_DEBUG and settings.TEST_ENDPOINT_URL:
        endpoint = settings.TEST_ENDPOINT_URL
    else:
        endpoint = instance.endpoint
    rs = requests.post(endpoint, data=message)
    if rs.status_code == 200:
        return True
