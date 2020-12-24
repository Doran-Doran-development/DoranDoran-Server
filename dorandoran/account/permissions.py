from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1:
            return True

        return request.user.uid == request.parser_context["kwargs"]["pk"]