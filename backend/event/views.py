from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import EventSerializer


class EventCreate(APIView):
    # authentication_classes = (TokenAuthentication, SessionAuthentication, )
    # permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            sessionid = request.headers.get("sessionid")
            print(request.session.get('user_id'))
            event = serializer.save()
            if event:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
