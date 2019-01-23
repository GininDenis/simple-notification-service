import logging

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.api.serializers import SubscriptionSerializer, ConfirmationSerializer
from apps.notifications.models import Subscription

logger = logging.getLogger(__file__)


class TestEndpointView(APIView):
    def post(self, request):
        logger.debug(request.POST)
        return Response(data={}, status=HTTP_200_OK)


class SubscriptionViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(topic__owner=self.request.user)


class ConfirmApiView(APIView):
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = serializer.validated_data['subscription']
        subscription.status = Subscription.STATUS_CHOICES.confirmed
        subscription.save(update_fields=['status'])

        return Response({})
