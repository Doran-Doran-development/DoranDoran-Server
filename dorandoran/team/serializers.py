import re
from rest_framework import serializers
from django.utils.translation import ugettext as _
from .models import Team, LinkedTeamUser
from account.models import User
from rest_framework.exceptions import ValidationError


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

    def validate_post_format(self, obj):
        teacher = obj["teacher"]
        project = obj["project"]

        # 유효한 교사 이메일인지 검사
        is_valid_teacher = self.is_teacher(teacher)
        if not is_valid_teacher:
            msg = _("User instance not exists")
            raise ValidationError(msg)

        # 프로젝트 이름이 형식에 맞는지 검사
        is_valid_project = self.is_right_project_name(project)
        if not is_valid_project:
            msg = _("is not valid project name format")
            raise ValidationError(msg)

        return obj

    def is_teacher(self, uid):
        queryset = User.objects.filter(uid=uid).filter(role=2)
        if not queryset.exists():
            return False
        return True

    def is_right_project_name(self, project):
        project_format = re.compile("(.+)[-](.+)")
        if not project_format.search(project):
            return False
        return True

    def is_empty_team(self):
        instance = self.initial_data
        if not instance:
            return True
        return False


class LinkedTeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedTeamUser
        fields = ("team_id", "user_id")
