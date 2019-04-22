import logging

from django.contrib.auth import login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import LoginSerializer, RestoreSessionSerializer

logger = logging.getLogger(__file__)


class TestEndpointApiView(APIView):
    def post(self, request):
        logger.debug(request.data)
        return Response()


class LoginApiView(APIView):
    def post(self, request):
        data = request.data
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

    def get(self, request):
        if request.user.is_authenticated:
            serialized_data = RestoreSessionSerializer(self.request.user).data
            serialized_data['is_authenticated'] = True
        else:
            serialized_data = RestoreSessionSerializer().data
            serialized_data['is_authenticated'] = False
        return Response(serialized_data)
