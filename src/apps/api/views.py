import logging

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core.exceptions import ObjectDoesNotExist

from apps.api.serializers import SubscriptionSerializer
from apps.notifications.models import Subscription

logger = logging.getLogger('api_debug')


class SubscriptionConfirmView(APIView):

    def post(self, request, token):
        logger.debug(token)
        return Response(data={'ok':'ok'}, status=HTTP_200_OK)

class TestEndpointView(APIView):

    def post(self, request):
        logger.debug(request.POST)
        return Response(data={}, status=HTTP_200_OK)


class SubscriptionViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class ConfirmApiView(APIView):

    def post(self, request):

        try:
            subscription_id = request.data['subscription_id']
            token = request.data['token']
            subscription = Subscription.objects.get(id=subscription_id)
        except (KeyError, ObjectDoesNotExist):
            return Response({}, status=HTTP_400_BAD_REQUEST)

        if subscription.token == token:
            subscription.status = Subscription.STATUS_CHOICES.confirmed
            subscription.save()
        else:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        return Response({}, status=HTTP_200_OK)
