from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http.response import HttpResponse
from mock import patch
from rest_framework import status

from apps.users import views
from apps.users.models import User
from apps.users.tokens import account_activation_token


class SignUpViewTestCase(TestCase):
    TEST_DATA = {
        'email': 'test@test.test',
        'password1': 'testpassword',
        'password2': 'testpassword'
    }

    def setUp(self):
        self.request_factory = RequestFactory()
        site = Site.objects.get_current()
        site.domain = 'http://test.com/'
        site.save()

    @patch.object(views.SignUpView, 'send_activation_email')
    def test_signup_successful(self, mocked_method_email):
        url = reverse('users:signup')
        response = self.client.post(url, data=self.TEST_DATA)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(User.objects.filter(
            email=self.TEST_DATA['email']).exists())

        user = User.objects.get(email=self.TEST_DATA['email'])
        self.assertFalse(user.is_active)
        mocked_method_email.assert_called_once_with(user)

    @patch.object(views.SignUpView, 'form_invalid',
                  return_value=HttpResponse())
    def test_signup_incorrect_email(self, mocked_form_invalid):
        url = reverse('users:signup')
        data = dict(self.TEST_DATA, email='test')
        self.client.post(url, data=data)

        mocked_form_invalid.assert_called_once()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=data['email'])


class ActivateAccountViewTestCase(TestCase):
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
        token = account_activation_token.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk)).decode('utf-8')
        self.view.get(self.request, uid, token)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
