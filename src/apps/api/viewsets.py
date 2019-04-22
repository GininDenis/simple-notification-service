from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from apps.api.filters import TopicFilter
from apps.api.serializers import (
    SubscriptionSerializer, ConfirmationSerializer, TopicSerializer
)
from apps.notifications.models import Subscription, Topic


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )

    @action(methods=['post'], detail=False, permission_classes=[])
    def confirm(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = serializer.validated_data['subscription']
        subscription.status = Subscription.STATUS_CHOICES.confirmed
        subscription.save(update_fields=['status'])

        return Response({"status": subscription.status})

    def get_queryset(self):
        return Subscription.objects.filter(
            topic__owner=self.request.user).order_by('pk')


class TopicViewSet(ModelViewSet):
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TopicFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user).order_by('pk')
