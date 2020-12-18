from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.authentication import CustomJSONWebTokenAuthentication

from .permissions import IsTeacherOrReadOnly
from .models import Room
from .serializers import RoomSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.db.models import Count
import json


class RoomViewSet(viewsets.ViewSet):

    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated & IsTeacherOrReadOnly]

    def list(self, request):

        queryset = Room.objects.all()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        obj = {
            "name": request.data["name"],
            "max_team": request.data["max_team"],
            "owner": request.user.email,
        }

        serializer = RoomSerializer(data=obj)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = Room.objects.get(pk=pk)
        serializer = RoomSerializer(queryset)
        return Response(serializer.data)

    def destroy(self, request,pk=None):
        instance = Room.objects.get(pk=pk)
        instance.delete()
        return Response({"message":"Success"},status=status.HTTP_204_NO_CONTENT)

    def update(self, request,pk=None):
        instance = Room.objects.get(pk=pk)
        instance.name = request.data["name"]
        instance.max_team = request.data["max_team"]
        instance.owner = request.user
        instance.save()
        return Response(request.data)
