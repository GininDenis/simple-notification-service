from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status

from apps.users.models import User


class LoginApiTestCase(TestCase):

    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'test'
    }

    login_url = reverse_lazy('api:login')
    logout_url = reverse_lazy('api:logout')

    def test_login_without_credentials(self):
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user(self):
        User.objects.create_user(**self.TEST_DATA)
        response = self.client.post(self.login_url, data=self.TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_active_user(self):
        user = User.objects.create_user(is_active=True, **self.TEST_DATA)
        response = self.client.post(self.login_url, data=self.TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('api:subscriptions-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_not_authenticated_user(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_authenticated_user(self):
        user = User.objects.create_user(is_active=True, **self.TEST_DATA)
        self.client.force_login(user)

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('api:subscriptions-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RestoreSessionApiTestCase(TestCase):

    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'test'
    }

    url = reverse_lazy('api:restore-session')

    def test_restore_session_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restore_session(self):
        user = User.objects.create_user(is_active=True, **self.TEST_DATA)
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.json().keys())
