from rest_framework.response import Response
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from .models import Team, LinkedTeamUser
from account.models import User
from .serializers import TeamSerializer, LinkedTeamUserSerializer
from account.authentication import CustomJSONWebTokenAuthentication
from .permissions import isTeacherOrNotDelete


# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
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

class ReadOnlyTeamViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        print(pk)
        team_obj = Team.objects.get(team_id=pk)
        members_obj = LinkedTeamUser.objects.filter(team_id=pk)
        print(team_obj.__dict__)
        team_serializer = self.get_serializer(data=team_obj.__dict__)
        members_serializer = LinkedTeamUserSerializer(data=members_obj, many=True)
        
        if team_serializer.is_empty_team():
            return Response(ValidationError("empty content"), status=204)
        
        if not team_serializer.is_valid():
            print("team error")
            return Response(team_serializer.errors)

        if not members_serializer.is_valid():
            print("member error")
            return Response(members_serializer.errors)
        
        print(team_serializer.validated_data)
        result_team_obj = team_serializer.validated_data
        result_team_obj.update(members_serializer.data)
        return Response(result_team_obj)
            
class TeamViewSet(viewsets.ViewSet):
    
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated & isTeacherOrNotDelete]

    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        if not serializer.validate_post_format(request.data):
            return Response(serializer.errors)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data, status=200)
    
    def destroy(self, request, pk=None):
        queryset = Team.objects.get(pk=pk)
        serializer = TeamSerializer(data=queryset)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.delete()
        return Response(status=202)
    
class MemberViewSet(viewsets.ViewSet):

    authentication_classes = [CustomJSONWebTokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]
     
    def create(self, request):
        serializer = LinkedTeamUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        serializer.save()
        obj = LinkedTeamUser.objects.filter(team_id=request.data["team_id"])
        members_obj = LinkedTeamUserSerializer(data=obj)
        return Response(members_obj.data, status=200)
    
    def retrieve(self, request, pk=None):
        quueryset = LinkedTeamUser.objects.filter(email=request.user.email)
        serializer = LinkedTeamUserSerializer(data=queryset, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        return Response(serializer.data, status=200)
    
    def destroy(self, request, pk=None):
        queryset = LinkedTeamUser.objects.get(pk=pk)
        serializer = LinkedTeamUserSerializer(data=queryset)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.delete()
        return Response(status=202)
