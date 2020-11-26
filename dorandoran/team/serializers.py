import re
from rest_framework.serializers import ModelSerializer
from .models import Team, LinkedTeamUser
from rest_framework.exceptions import ValidationError


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team

    def is_valid_project(self, value):
        p = re.compile("\B-\B")
        if not p.search(value):
            return ValidationError("대회명-팀명 형식에 맞추어야 합니다.")


class LinkedTeamUserSerializer(ModelSerializer):
    class Meta:
        model = LinkedTeamUser
