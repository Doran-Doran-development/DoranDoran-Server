import re
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from account.models import User


class TeamPermission(BasePermission):
    def is_teacher(self, value):
        queryset = User.objects.filter(eamil=value).filter(is_teacher=True)
        if not queryset.exists():
            return
        return True

    def is_valid_project_name(self, value):
        teamname_format = re.compile("\B-\B")
        if not teamname_format.search(value):
            return False
        return True