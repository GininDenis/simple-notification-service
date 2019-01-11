from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = 'apps.users'
    verbose_name = _('Authentication')
