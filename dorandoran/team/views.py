from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from .models import Team, LinkedTeamUser
from account.models import User
from .serializers import TeamSerializer, LinkedTeamUserSerializer

# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    team_queryset = Team.objects.all()

    # 팀 생성
    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.validate(request.data):
            serializer.save()
            return Response({"message": "register success"}, status=200)

    # 모든 팀 리스트
    def list(self, request):

        pass

    # 해당 팀 정보
    def retrieve(self, request, pk=None):
        team_info = get_object_or_404(team_queryset, pk)

        if team_info == Http404:
            return Response("존재하지 않는 팀 입니다", status=404)
        return Response(team_info, status=200)

    # 특정 유저의 팀정보 가져오기
    @action(detail=True, methods=["get"])
    def get_own_team(self, request, eamil=None):

        pass

    # 팀 삭제
    def destory(self, request, pk=None):

        pass


class LinkedTeamUserViewSet(viewsets.ModelViewSet):

    # 팀원 추가
    def create(self, request):
        return

    # 팀원 삭제
    def destroy(self, request, pk=None):
        return