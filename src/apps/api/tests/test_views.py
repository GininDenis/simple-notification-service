from collections import namedtuple

from django.test import TestCase
from model_mommy import mommy

from apps.notifications.models import Subscription
from apps.api.views import ConfirmSubscriptionApiView


class ConfirmSubscriptionApiTestCase(TestCase):

    def test_post(self):
        subscription = mommy.make(Subscription)
        view = ConfirmSubscriptionApiView()
        request = namedtuple('request', 'data')
        request.data = {
            'subscription': subscription.pk,
            'token': subscription.token
        }
        view.post(request)
        subscription.refresh_from_db()
        self.assertEqual(subscription.status,
                         Subscription.STATUS_CHOICES.confirmed)
