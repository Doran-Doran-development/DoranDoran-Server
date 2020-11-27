import re
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from account.models import User


class TeamPermission(BasePermission):
    def is_teacher(self, value):
        try:
            queryset = User.objects.get(email=value)

            if not queryset["is_teacher"]:
                return False

        except User.DoesNotExist:
            return

        return True

    def is_valid_project_name(self, value):
        teamname_format = re.compile("\B-\B")
        if not teamname_format.search(value):
            return False
        return True