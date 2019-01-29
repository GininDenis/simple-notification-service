from django.test import TestCase
from django.db.models.signals import post_save

from apps.notifications.models import Subscription
from apps.notifications.signal_handlers import confirm_subscription


class NotificationConfigTestCase(TestCase):

    def test_ready(self):
        self.assertIn(confirm_subscription,
                      post_save._live_receivers(sender=Subscription))
