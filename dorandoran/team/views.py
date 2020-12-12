from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from .models import Team, LinkedTeamUser
from account.models import User
from .serializers import TeamSerializer, LinkedTeamUserSerializer
from account.authentication import CustomJSONWebTokenAuthentication
from room.permissions import IsTeacherOrReadOnly
from rest_framework import permissions

# Create your views here.


class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # 팀 생성
    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.validate(request.data) and serializer.is_valid(request.data):
            serializer.save()
            return Response(serializer.data, status=200)


class TeamDestroyView(generics.DestroyAPIView):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated & IsTeacherOrReadOnly]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamRetrieveView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    

class TeamJoinView(generics.CreateAPIView):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = LinkedTeamUser.objects.all()
    serializer_class = LinkedTeamUserSerializer


class TeamOutView(generics.DestroyAPIView):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = LinkedTeamUser.objects.all()
    serializer_class = LinkedTeamUserSerializer

    def destroy(self, request, email=None, team_id=None):
        serializer = LinkedTeamUserSerializer(data={"email": email, "team_id": team_id})
        if not serializer.is_valid():
            return Response({"msg": "invalid email, "}, status=400)


class TeamView(generics.ListAPIView):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, email=None):
        queryset = LinkedTeamUser.objects.filter(email=email)
        if not queryset:
            return Response(
                {"msg": "{} never joined any team".format(email)}, status=404
            )
        serializer = LinkedTeamUserSerializer(data=queryset)
        return Response(serializer.data, status=200)
