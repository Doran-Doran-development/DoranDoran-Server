from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if request.user.role == 1:
                return True

            return request.user.uid == request.parser_context["kwargs"]["pk"]

        return False