from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SnsConfig(AppConfig):
    name = 'apps.notifications'
    verbose_name = _('notifications')
