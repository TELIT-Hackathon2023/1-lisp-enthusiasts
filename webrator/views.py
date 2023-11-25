from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AnalyticsInputSerializer

import requests
import os


class HelloWorldView(APIView):
    def get(self, request):
        data = {'message': 'Hello, World!'}
        return Response(data)
    

class AnalyticsView(APIView):
    def get(self, request):
        serializer = AnalyticsInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}'

        r = requests.get(x)
        final = r.json()
        return Response({"message": final}, status=status.HTTP_200_OK)
