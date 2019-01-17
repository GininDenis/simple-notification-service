from django.urls import reverse
from django.conf import settings

from apps.notifications.tasks import send_subscription_confirmation
from apps.notifications.tokens import subscription_activation_token


def confirm_subscription(**kwargs):
    instance = kwargs.get('instance')
    message = {
        'type': 'SubscriptionConfirmation',
        'subscription_url': '',
        'token': instance.token,
        'message': 'You have to confirm subscription, please follow the ‘subscription_url’ link'
    }

    token = subscription_activation_token.make_token(instance)
    activate_url = reverse('api:subscription-confirm',
                           kwargs={'token': token})

    message['subscription_url'] = activate_url

    if settings.SUBSCRIPTION_ENDPOINT_DEBUG and settings.TEST_ENDPOINT_URL:
        endpoint = settings.TEST_ENDPOINT_URL
    else:
        endpoint = instance.endpoint
    send_subscription_confirmation.delay(message, endpoint)
