from django.test import TestCase
from model_mommy import mommy

from apps.notifications.forms import SubscriptionUpdateForm
from apps.notifications.models import Topic
from apps.users.models import User


class SubscriptionUpdateFormTest(TestCase):


    def setUp(self):
        for user in mommy.make(User, _quantity=3):
            mommy.make(Topic,owner=user, _quantity=3)


    def test_init(self):
        user = User.objects.first()
        form = SubscriptionUpdateForm(user=user)

        self.assertEqual(list(form.fields['topic'].queryset),
                         list(Topic.objects.filter(owner__id=user.pk)))