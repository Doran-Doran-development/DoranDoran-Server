from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
import json
from django.core import serializers

from account.authentication import CustomJSONWebTokenAuthentication
from .models import Team, LinkedTeamUser
from .serializers import TeamSerializer, LinkedTeamUserSerializer
from .permissions import isTeacherOrNotDelete


# Create your views here.


class TeamViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated & isTeacherOrNotDelete]


class TeamDetailView(generics.GenericAPIView):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        team_with_member = Team.objects.raw(
            """
        SELECT 
            T.team_id,
            T.project,
            T.description,
            T.teacher_id,
            (
                SELECT
                    uid_id
                FROM
                    linkedteamuser
                WHERE
                    team_id_id = 2
            )
            FROM
                Team as T
            WHERE
                T.team_id = 2;
        """.format(
                self.kwargs["pk"]
            )
        )
        # team_with_membe = Team.objects.prefetch_related(
        #     Prefetch(
        #         "linkedteamuser_set", queryset=LinkedTeamUser.objects.filter(team_id=pk)
        #     )
        # ).filter(team_id=pk)
        data = serializers.serialize("json", team_with_member)
        return data


class MemberViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = LinkedTeamUser.objects.all()
    serializer_class = LinkedTeamUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    @action(detail=True, methods=["get"])
    def detailed(self, request, pk=None):
        queryset = LinkedTeamUser.objects.filter(team_id=pk)
        members_serializer = LinkedTeamUserSerializer(data=queryset, many=True)
        if not members_serializer.is_valid():
            raise ValidationError(code=400)
        return Response(members_serializer.data, status=200)