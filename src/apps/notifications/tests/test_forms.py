from django.test import TestCase
from django.db.models.signals import post_save

from apps.notifications.forms import SubscriptionUpdateForm


class SubscriptionUpdateFormTest(TestCase):

    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword',
        'first_name': 'John',
        'last_name': 'Smith'
    }

    def setUp(self):
        # TODO: Create some amount of topics and users
        pass

    def test_init(self):
        # form = SubscriptionUpdateForm()
        pass
