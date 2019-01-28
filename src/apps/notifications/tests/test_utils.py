from random import randint

from django.test import TestCase

from apps.notifications.utils import generate_key


class UtilsTest(TestCase):

    def test_generate_key(self):

        length = randint(1,100)
        key = generate_key(length)
        self.assertEqual(len(key), length)
        self.assertIsInstance(key, str)
