from django.test import TestCase

from apps.users.models import User


class UserManagerTest(TestCase):
    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword'
    }

    def setUp(self):
        self.test_manager = User.objects

    def validate_user(self, user):
        self.assertEqual(user.email, self.TEST_DATA['email'])
        self.assertEqual(user.check_password(self.TEST_DATA['password']), True)

    def test_create_user(self):
        user = self.test_manager.create_user(**self.TEST_DATA)
        self.validate_user(user)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_create_superuser(self):
        user = self.test_manager.create_superuser(**self.TEST_DATA)
        self.validate_user(user)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)