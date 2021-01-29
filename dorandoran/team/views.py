from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.http import Http404, HttpResponseBadRequest
from django.forms.models import model_to_dict
import json
import jwt
from django.http import JsonResponse

from account.authentication import CustomJSONWebTokenAuthentication, jwt_get_uid_from_payload_handler
from account.models import User
from django.conf import settings
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

        if len(queryset) == 1:
            member_obj = model_to_dict(queryset.first())

            return JsonResponse(member_obj) 
        else:
            members_serializer = LinkedTeamUserSerializer(queryset, many=True)

        return Response(members_serializer.data, status=200)

