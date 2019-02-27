import logging

from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import LoginSerializer, RestoreSessionSerializer

logger = logging.getLogger(__file__)


class TestEndpointApiView(APIView):
    def post(self, request):
        logger.debug(request.POST)
        return Response()


class LoginApiView(APIView):
    def post(self, request):
        data = request.POST
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'status': 'Login successful'})


class LogoutApiView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestoreSessionApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(RestoreSessionSerializer(self.request.user).data)
