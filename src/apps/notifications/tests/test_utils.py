from django.test import TestCase

from apps.notifications.utils import generate_key


class UtilsTestCase(TestCase):

    def test_generate_key(self):

        length = 15
        key = generate_key(length)
        self.assertIsInstance(key, str)
        self.assertEqual(len(key), length)
