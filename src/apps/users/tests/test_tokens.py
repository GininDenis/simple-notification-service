from django.test import TestCase

from apps.users.tokens import AccountActivationTokenGenerator
from apps.users.models import User


class TokenTestCase(TestCase):
    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword'
    }

    def setUp(self):
        self.user = User.objects.create(**self.TEST_DATA)

    def test_make_hash_value(self):
        generator = AccountActivationTokenGenerator()
        timestamp = generator._num_days(generator._today())
        hash_value = generator._make_hash_value(self.user, timestamp)
        self.assertTrue(hash_value.startswith(str(self.user.pk)))
        self.assertIn(str(timestamp), hash_value)
        self.assertTrue(str(self.user.is_active) in hash_value)
