from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class SubscriptionActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, subscription, timestamp):
        return (
            six.text_type(subscription.pk) + six.text_type(timestamp) +
            six.text_type(subscription.status)
        )

subscription_activation_token = SubscriptionActivationTokenGenerator()
