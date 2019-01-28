from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from model_mommy import mommy

from apps.notifications.tokens import subscription_activation_token
from apps.notifications import views
from apps.notifications.models import Subscription
from apps.users.models import User


class SubscriptionConfirmTestCase(TestCase):

    def setUp(self):
        self.subscription = mommy.make(Subscription)
        self.user = mommy.make(User)

        self.request_factory = RequestFactory()
        self.request = self.request_factory.get(reverse('admin:login'))
        self.request.user = self.user
        self.view = views.SubscriptionConfirmView(request=self.request)

    def test_post(self):
        token = subscription_activation_token.make_token(self.subscription)
        uid = urlsafe_base64_encode(force_bytes(self.subscription.pk)).decode(
            'utf-8')
        self.view.post(uid, token)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.status,
                         Subscription.STATUS_CHOICES.confirmed)
