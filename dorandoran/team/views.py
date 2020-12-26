from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from account.authentication import CustomJSONWebTokenAuthentication
from .models import Team, LinkedTeamUser
from .serializers import TeamSerializer, LinkedTeamUserSerializer
from .permissions import isTeacherOrNotDelete


# Create your views here.

class TeamListAPI(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [CustomJSONWebTokenAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=200)

class TeamDetailAPI(generics.RetrieveAPIView):
    authentication_classes = [CustomJSONWebTokenAuthentication]

    # 팀 상세 정보 확인
    def retrieve(self, request, pk=None):
        team_obj = Team.objects.get(team_id=pk)
        members_obj = LinkedTeamUser.objects.filter(team_id=pk)

        team_serializer = TeamSerializer(data=team_obj.__dict__)
        members_serializer = LinkedTeamUserSerializer(data=members_obj, many=True)

        if team_serializer.is_empty_team():
            return Response(ValidationError("empty content"), status=204)

        if not team_serializer.is_valid():
            print("team error")
            return Response(team_serializer.errors)

        if not members_serializer.is_valid():
            print("member error")
            return Response(members_serializer.errors)

        result_team_obj = team_serializer.validated_data
        result_team_obj.update(members_serializer.data)
        return Response(result_team_obj)


# class ReadOnlyTeamViewSet(viewsets.ReadOnlyModelViewSet):
#
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     authentication_classes = [CustomJSONWebTokenAuthentication]
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data,status=200)
#     # 팀 기본 정보 모두 확인 def list(self, request, *args, **kwargs):
#
#     # 팀 상세 정보 확인
#     def retrieve(self, request, pk=None):
#
#         team_obj = Team.objects.get(team_id=pk)
#         members_obj = LinkedTeamUser.objects.filter(team_id=pk)
#
#         team_serializer = self.get_serializer(data=team_obj.__dict__)
#         members_serializer = LinkedTeamUserSerializer(data=members_obj, many=True)
#
#         if team_serializer.is_empty_team():
#             return Response(ValidationError("empty content"), status=204)
#
#         if not team_serializer.is_valid():
#             print("team error")
#             return Response(team_serializer.errors)
#
#         if not members_serializer.is_valid():
#             print("member error")
#             return Response(members_serializer.errors)
#
#         result_team_obj = team_serializer.validated_data
#         result_team_obj.update(members_serializer.data)
#         return Response(result_team_obj)
            
class TeamViewSet(viewsets.ViewSet):
    
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated & isTeacherOrNotDelete]

    # 팀 생성
    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        if not serializer.validate_post_format(request.data):
            return Response(serializer.errors)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data, status=200)
    
    # 팀 삭제
    def destroy(self, request, pk=None):
        instance = Team.objects.get(pk=pk)
        instance.delete()
        return Response({"message": "no content"}, status=204)
    
class MemberViewSet(viewsets.ViewSet):

    authentication_classes = [CustomJSONWebTokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    # 멤버 추가
    def create(self, request, *args, **kwargs):
        serializer = LinkedTeamUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        obj = LinkedTeamUser.objects.filter(team_id=request.data["team_id"])
        members_obj = LinkedTeamUserSerializer(data=obj)
        return Response(members_obj.data, status=200)
    
    # 팀 멤버 모두 확인
    def list(self, request):
        quueryset = LinkedTeamUser.objects.filter(email=request.user.email)
        serializer = LinkedTeamUserSerializer(data=quueryset, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        return Response(serializer.data, status=200)
    
    # 멤버 삭제
    def destroy(self, request, pk=None):
        instance = LinkedTeamUserSerializer.objects.get(pk=pk)
        instance.delete()
        return Response({"message": "no content"}, status=204)
