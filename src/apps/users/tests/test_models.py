from django.test import TestCase
from django.core import mail

from apps.users.models import User


class UserModelTestCase(TestCase):

    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword',
        'first_name': 'John',
        'last_name': 'Smith'
    }

    def setUp(self):
        self.user = User.objects.create(**self.TEST_DATA)

    def test_clean(self):
        self.user.email = ' test@ww.ss   '
        self.user.clean()
        self.assertEqual(self.user.email, 'test@ww.ss')

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'John Smith')

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'John')

    def test_send_mail(self):
        self.user.email_user('Test Subject', 'Test Message')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
