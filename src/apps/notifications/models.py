from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from model_utils.choices import Choices
from model_utils.models import TimeStampedModel

from apps.notifications.utils import generate_key
from apps.users.models import User


class Token(TimeStampedModel):
    key = models.CharField(_('Key'), max_length=10, primary_key=True,
                           default=generate_key)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_('User')
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    def __str__(self):
        return self.key


class Topic(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),
                              on_delete=models.CASCADE,
                              related_name='topics')

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __str__(self):
        return self.title


class Subscription(TimeStampedModel):
    PROTOCOL_CHOICES = Choices(
        ('http', _('HTTP')),
        ('https', _('HTTPS'))
    )

    STATUS_CHOICES = Choices(
        ('pending', _('Pending')),
        ('canceled', _('Canceled')),
        ('confirmed', _('Confirmed'))
    )

    topic = models.ForeignKey(Topic, verbose_name=_('Topic'),
                              on_delete=models.CASCADE,
                              related_name='subscriptions')
    token = models.CharField(_('Token'), max_length=10, default=generate_key)
    protocol = models.CharField(_('Protocol'), max_length=5,
                                choices=PROTOCOL_CHOICES)
    status = models.CharField(_('Status'), max_length=9, editable=False,
                              choices=STATUS_CHOICES,
                              default=STATUS_CHOICES.pending)
    endpoint = models.URLField(_('Endpoint'))

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
