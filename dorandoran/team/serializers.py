import re
from rest_framework.serializers import ModelSerializer, Serializer
from django.utils.translation import ugettext as _
from .models import Team, LinkedTeamUser
from rest_framework.exceptions import ValidationError
from .permissions import TeamPermission


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ("team_id", "project", "description", "teacher")

    def validate(self, req):
        teacher = req["teacher"]
        project = req["project"]

        is_valid_teacher = TeamPermission.is_teacher(teacher)
        if is_teacher == None:
            msg = _("User instance not exists")
            raise ValidationError(msg)

        is_valid_project = TeamPermission.is_valid_project_name(project)

        if not is_valid_project:
            msg = _("is not valid project name format")
            raise ValidationError(msg)

        return True


class LinkedTeamUserSerializer(ModelSerializer):
    class Meta:
        model = LinkedTeamUser
