from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AnalyticsInputSerializer, PersonaInputSerialier
from .services import get_text_from_website, parse_json
from config.settings import client

import requests
import os


class HelloWorldView(APIView):
    def get(self, request):
        data = {'message': 'Hello, World!'}
        return Response(data)


class AnalyticsView(APIView):
    def post(self, request):
        serializer = AnalyticsInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        analytics = os.environ.get('ANALYTICS')
        url = serializer.validated_data['url']
        r = requests.get(analytics + '=' + url)
        final = r.json()

        parsed_data = parse_json(final)

        return Response(parsed_data, status=status.HTTP_200_OK)


class PersonaView(APIView):
    def post(self, request):
        serializer = PersonaInputSerialier(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        res = get_text_from_website(url, url, set())

        messages = [
            {"role": "system", "content": res},
            {"role": "user", "content": "This is a text content of a website. I want to learn who is the website adressed to. Write a list of personas that the website was created for. For each persona write the name followed by three underscores followed by a short description"}
        ]

        response = client.chat.completions.create(
            model='gpt-4',
            messages=messages
        )

        ans = response.choices[0].message.content.split('\n')

        response = {}

        for elm in ans:
            if len(elm) > 3:
                values = elm.split('___')
                response[values[0]] = values[1]

        return Response(response)
