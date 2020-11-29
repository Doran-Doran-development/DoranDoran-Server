from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count
import json


class RoomViewSet(viewsets.ViewSet):
    def list(self, request):

        queryset = Room.objects.all()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        obj = {
            "name": request.data["name"],
            "max_team": request.data["max_team"],
            "owner": request.user.id,
        }

        serializer = RoomSerializer(data=obj)

        if not serializer.is_valid():
            return Response(serializer.errors)

        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Room.objects.get(pk=pk)
        serializer = RoomSerializer(queryset)
        return Response(serializer.data)
