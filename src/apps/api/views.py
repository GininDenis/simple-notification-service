from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class SubscriptionConfirmView(APIView):

    def post(self, request, token):
        print(hash)
        return Response(data={'ok':'ok'}, status=HTTP_200_OK)

class TestEndpointView(APIView):

    def post(self, request):
        print(request.POST)
        return Response(data={}, status=HTTP_200_OK)
