from django.test import TestCase

from apps.users.models import User


class UserManagerTestCase(TestCase):
    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword'
    }

    def setUp(self):
        self.test_manager = User.objects

    def validate_user(self, user):
        self.assertEqual(user.email, self.TEST_DATA['email'])
        self.assertTrue(user.check_password(self.TEST_DATA['password']))

    def test_create_user(self):
        user = self.test_manager.create_user(**self.TEST_DATA)
        self.validate_user(user)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = self.test_manager.create_superuser(**self.TEST_DATA)
        self.validate_user(user)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
