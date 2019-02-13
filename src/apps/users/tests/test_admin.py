from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from apps.users.models import User
from apps.users.admin import UserAdmin


class UserAdminTestCase(TestCase):
    TEST_DATA = {
        'email': 'test@test.test',
        'password': 'testpassword',
        'first_name': 'John',
        'last_name': 'Smith'
    }

    def setUp(self):
        self.user = User.objects.create(**self.TEST_DATA)
        self.site = AdminSite()
        self.ua = UserAdmin(User, self.site)
        self.rf = RequestFactory()

    def test_get_fieldsets(self):
        template = (
            (
                None,
                {
                    'classes': ('wide', ),
                    'fields': ('email', 'password1', 'password2')
                }
            ),
        )

        request = self.rf.get(reverse('admin:login'))
        self.assertEqual(self.ua.get_fieldsets(request), template)

    def test_get_form(self):
        request = self.rf.get(reverse('admin:login'))
        self.ua.get_form(request)
