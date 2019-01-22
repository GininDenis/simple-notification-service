from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from apps.notifications.signal_handlers import confirm_subscription

class NotificationConfig(AppConfig):
    name = 'apps.notifications'
    verbose_name = _('Notifications')

    def ready(self):
        subscription = self.get_model('Subscription')
        post_save.connect(confirm_subscription, sender=subscription)
