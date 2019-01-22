from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from apps.notifications.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['protocol', 'endpoint', 'topic', 'id']
        extra_kwargs = {
            'protocol': {
                'write_only': True
            },
            'endpoint': {
                'write_only': True
            },
            'topic': {
                'write_only': True
            }
        }


class ConfirmationSerializer(serializers.Serializer):

    subscription = serializers.PrimaryKeyRelatedField(
        queryset=Subscription.objects.all()
    )
    token = serializers.CharField()

    def validate(self, attrs):
        subscription = attrs['subscription']
        token = attrs['token']

        if subscription.token != token:
            raise ValidationError({'token': _('Invalid token')})
        return attrs
