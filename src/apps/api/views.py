import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

logger = logging.getLogger('api_debug')


class SubscriptionConfirmView(APIView):

    def post(self, request, token):
        logger.debug(token)
        return Response(data={'ok':'ok'}, status=HTTP_200_OK)

class TestEndpointView(APIView):

    def post(self, request):
        logger.debug(request.POST)
        return Response(data={}, status=HTTP_200_OK)
