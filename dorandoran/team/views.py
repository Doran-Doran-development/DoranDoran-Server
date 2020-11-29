from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from .models import Team, LinkedTeamUser
from account.models import User
from .serializers import TeamSerializer, LinkedTeamUserSerializer

# Create your views here.


class TeamListCreateAPI(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    # 팀 생성
    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.validate(request.data) and serializer.is_valid(request.data):
            serializer.save()
            return Response(serializer.data, status=200)


class TeamRetrieveDestroyAPI(generics.RetrieveDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class LinkedTeamUserViewSet(viewsets.ModelViewSet):

    # 팀원 추가
    def create(self, request):
        return

    # 팀원 삭제
    def destroy(self, request, pk=None):
        return
