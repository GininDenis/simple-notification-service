import requests
from django.urls import reverse_lazy

from apps.notifications.tokens import subscription_activation_token


def send_subscription_confirmation(sender, **kwargs):
    instance = kwargs.get('instance')
    message = {
        'type': 'SubscriptionConfirmation',
        'subscription_url': '',
        'token': instance.token,
        'message': 'You have to confirm subscription, please follow the ‘subscription_url’ link'

    }

    token = subscription_activation_token.make_token(instance)
    message['subscription_url'] = reverse_lazy('api:subscription-confirm',
                                               kwargs={'token': token})

    rs = requests.post(instance.endpoint, data=message)
    print(rs.status_code)