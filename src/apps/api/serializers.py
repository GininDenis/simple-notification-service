from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.notifications.models import Subscription, Topic
from apps.users.models import User


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['protocol', 'endpoint', 'topic', 'id']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'owner']


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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):

        user = authenticate(**attrs)
        if user:
            attrs.update({'user': user})
            return attrs
        else:
            raise ValidationError('Invalid user')


class RestoreSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'email']
