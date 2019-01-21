from rest_framework.serializers import ModelSerializer, CharField

from apps.notifications.models import Subscription


class SubscriptionSerializer(ModelSerializer):
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
