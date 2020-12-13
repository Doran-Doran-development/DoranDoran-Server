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

class ReadOnlyTeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        team_obj = Team.objects.get(team_id=pk)
        members_obj = Team.objects.filter(team_id=pk)

        team_serializer = TeamSerializer(data=team_obj)
        members_serializer = LinkedTeamUserSerializer(data=members_obj, many=True)
        if team_serializer.is_valid() and members_serializer.is_valid():
            
            return Response(team_serializer.data, members_serializer.data) 
            
class TeamViewSet(viewsets.ViewSet):
    
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated & isTeacherOrNotDelete]

    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.validate(request.data) and serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
    
    def destroy(self, request, *args, **kwargs):
        queryset = Team.objects.get(pk=pk)
        serializer = TeamSerializer(data=queryset)
        if not serializer.is_valid():
            return ValidationError()
        serializer.delete()
        return Response(status=202)
    
class MemberViewSet(viewsets.ViewSet):

    authentication_classes = [CustomJSONWebTokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated & isTeacherOrNotDelete]

    def list(self, request, *args, **kwargs):
        quueryset = LinkedTeamUser.objects.filter(email=request.user.email)
        serializer = LinkedTeamUserSerializer(data=queryset)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
    
    def destroy(self, request, pk=None):
        queryset = LinkedTeamUser.objects.get(pk=pk)
        serializer = LinkedTeamUserSerializer(data=queryset)
        if serializer.is_valid():
            serializer.delete()
            return Response(status=202)

    def create(self, request):
        serializer = LinkedTeamUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)


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

# class TeamRetrieveDestroyView(generics.RetrieveDestroyAPIView):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     authentication_classes = [CustomJSONWebTokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated & Is]


# class TeamJoinView(generics.CreateAPIView):
#     authentication_classes = [CustomJSONWebTokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = LinkedTeamUser.objects.all()
#     serializer_class = LinkedTeamUserSerializer


# class TeamOutView(generics.DestroyAPIView):
#     authentication_classes = [CustomJSONWebTokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = LinkedTeamUser.objects.all()
#     serializer_class = LinkedTeamUserSerializer

#     def destroy(self, request, email=None, team_id=None):
#         serializer = LinkedTeamUserSerializer(data={"email": email, "team_id": team_id})
#         if not serializer.is_valid():
#             return Response({"msg": "invalid email, "}, status=400)


# class TeamView(generics.ListAPIView):
#     authentication_classes = [CustomJSONWebTokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def list(self, request, email=None):
#         queryset = LinkedTeamUser.objects.filter(email=email)
#         if not queryset:
#             return Response(
#                 {"msg": "{} never joined any team".format(email)}, status=404
#             )
#         serializer = LinkedTeamUserSerializer(data=queryset)
#         return Response(serializer.data, status=200)
