import json

from collections import namedtuple

from django.test import TestCase, override_settings
from django.contrib.sites.models import Site
from model_mommy import mommy
from mock import patch

from apps.notifications.tasks import get_endpoint, create_message, \
    send_subscription_confirmation
from apps.notifications.models import Subscription

ENDPOINT_URL = 'http://test.test/test/'


class SubscriptionConfirmationTestCase(TestCase):

    def setUp(self):
        self.subscription = mommy.make(Subscription)
        site = Site.objects.get_current()
        site.domain = 'http://test.com/'
        site.save()

    @override_settings(TEST_ENDPOINT_URL=ENDPOINT_URL)
    def test_get_endpoint(self):
        instance = namedtuple('instanse', 'endpoint')
        instance.endpoint = 'http://enpoint_test.com/test/'
        with self.settings(SUBSCRIPTION_ENDPOINT_DEBUG=False):
            endpoint = get_endpoint(instance)
            self.assertEqual(endpoint, instance.endpoint)
        with self.settings(SUBSCRIPTION_ENDPOINT_DEBUG=True):
            endpoint = get_endpoint(instance)
            self.assertEqual(endpoint, ENDPOINT_URL)

    def test_create_message(self):
        instance, message = create_message(self.subscription.id)
        self.assertEqual(instance, self.subscription)
        self.assertEqual(message['token'], self.subscription.token)
        self.assertEqual(message['subscription_id'], self.subscription.pk)

    @patch('apps.notifications.tasks.requests.post')
    def test_send_subscription_confirmation(self, mock_post):
        error_msg = lambda : {'Status': 'Error'}
        response = namedtuple('response', 'status_code, json')
        response.status_code = 400
        response.json = error_msg
        mock_post.return_value = response
        send_subscription_confirmation(self.subscription.id)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.error_msg, json.dumps(error_msg()))
        