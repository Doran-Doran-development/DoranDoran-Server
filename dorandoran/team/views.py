from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.http import Http404, HttpResponseBadRequest
from django.forms.models import model_to_dict
import json
import jwt
from django.http import JsonResponse

from account.authentication import (
    jwt_get_uuid_from_payload_handler,
)
from account.models import User
from config.settings.dev import JWT_AUTH
from .models import Team, LinkedTeamUser
from .serializers import TeamSerializer, LinkedTeamUserSerializer
from .permissions import IsTeacherOrNotDelete


# Create your views here.


class TeamViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated & IsTeacherOrNotDelete]


class MemberViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = LinkedTeamUser.objects.all()
    serializer_class = LinkedTeamUserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        team_num = self.get_queryset().filter(team_id=request.data["team_id"])

        if len(team_num) > 11:  # 팀원수 12명 제한
            return Response(
                "This team is already full.", status=status.HTTP_406_NOT_ACCEPTABLE
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["get"])
    def detailed(self, request, pk=None):
        queryset = LinkedTeamUser.objects.filter(team_id=pk)
        if len(queryset) == 0:
            return Response(
                "There's no matching info", status=status.HTTP_204_NO_CONTENT
            )
        if len(queryset) == 1:
            member_obj = model_to_dict(queryset.first())
            return JsonResponse(member_obj)
        else:
            members_serializer = LinkedTeamUserSerializer(queryset, many=True)

        return Response(members_serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None).split()[1]
        payload = jwt.decode(
            token, JWT_AUTH["JWT_SECRET_KEY"], JWT_AUTH["JWT_ALGORITHM"]
        )
        token_uid = jwt_get_uid_from_payload_handler(payload)
        try:
            instance = LinkedTeamUser.objects.get(
                team_id=self.kwargs["pk"], uid=token_uid
            )
        except Exception as e:
            return Response(
                "There's no matching info", status=status.HTTP_404_NOT_FOUND
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
