import re
from rest_framework import serializers
from django.utils.translation import ugettext as _
from .models import Team, LinkedTeamUser
from account.models import User
from rest_framework.exceptions import ValidationError
from .permissions import TeamPermission


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

    def validate(self, req):

        teacher = req["is_teacher"]
        project = req["project"]

        #유효한 교사 이메일인지 검사
        is_valid_teacher = self.is_teacher(teacher)
        if not is_valid_teacher:
            msg = _("User instance not exists")
            raise ValidationError(msg)

        #프로젝트 이름이 형식에 맞는지 검사
        is_valid_project = self.is_valid_project_name(project)
        if not is_valid_project:
            msg = _("is not valid project name format")
            raise ValidationError(msg)

        return True

    def is_teacher(self, email):
        queryset = User.objects.filter(email=email).filter(is_teacher=True)
        if not queryset.exists():
            return False
        return True

    def is_valid_project_name(self, project):
        project_format = re.compile("(.+)[-](.+)")
        if not project_format.search(project__name):
            return False
        return True

class LinkedTeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedTeamUser
        fields = "__all__"
