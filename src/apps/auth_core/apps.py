from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = 'apps.auth_core'
    verbose_name = _('Authentication')
