from django.test import TestCase

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
        full_name = '{} {}'.format(self.TEST_DATA['first_name'],
                                   self.TEST_DATA['last_name'])
        self.assertEqual(self.user.get_full_name(), full_name)

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(),
                         self.TEST_DATA['first_name'])
