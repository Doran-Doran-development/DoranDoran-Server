import re
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from account.models import User


class TeamPermission(BasePermission):
    def is_teacher(value):
        queryset = User.objects.filter(email=value).filter(is_teacher=True)
        if not queryset.exists():
            return
        return True

    def is_valid_project_name(value):
        project_format = re.compile("(.+)[-](.+)")
        if not project_format.search(value):
            return False
        return True