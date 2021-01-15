from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

from account.authentication import CustomJSONWebTokenAuthentication
from .models import Team, LinkedTeamUser
from .serializers import TeamSerializer, LinkedTeamUserSerializer
from .permissions import isTeacherOrNotDelete


# Create your views here.

class TeamViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated & isTeacherOrNotDelete]

    @action(detail=True, methods=["get"])
    def detailed(self, request, pk=None):
        team_obj = Team.objects.get(team_id=pk)
        members_obj = LinkedTeamUser.objects.filter(team_id=pk)
        print("team", team_obj)
        print("member", members_obj)

        team_serializer = TeamSerializer(data=team_obj)
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


