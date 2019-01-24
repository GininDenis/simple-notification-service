from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from django.core import mail
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mock import patch

from apps.users import views
from apps.users.models import User
from apps.users.tokens import account_activation_token


class SignUpViewTest(TestCase):
    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword'
    }

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(**self.TEST_DATA)
        self.request = self.request_factory.get(reverse('admin:login'))
        self.request.user = self.user
        self.view = views.SignUpView(request=self.request)
        site = Site.objects.get_current()
        site.domain = 'http://test.com/'
        site.save()


    def test_send_activation_email(self):
        self.view.send_activation_email(self.user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate Your MySite Account')


class ActivateAccountViewTest(TestCase):
    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword'
    }

    def setUp(self):
        self.user = User.objects.create(**self.TEST_DATA)
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get(reverse('admin:login'))
        self.view = views.ActivateAccountView(request=self.request)

    @patch('apps.users.views.login')
    @patch('apps.users.views.messages.add_message')
    def test_get(self, mock_message, mock_login):
        mock_login.return_value = None
        token = account_activation_token.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk)).decode('utf-8')
        self.view.get(self.request, uid, token)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
