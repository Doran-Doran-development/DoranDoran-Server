from rest_framework import permissions


class IsTeacherOrNotDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return bool(request.user.role == 2)
        return True
