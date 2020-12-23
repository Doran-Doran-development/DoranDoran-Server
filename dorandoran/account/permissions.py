from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadAndCreate(BasePermission):
    def has_permission(self, request, view):
        ALLOW_METHODS = ("GET", "HEAD", "OPTIONS", "POST")
        ISOWNER_METHODS = ("DELETE", "PUT")

        if request.method in ALLOW_METHODS:  # GET, HEAD, OPTIONS
            return True
        elif request.method in ISOWNER_METHODS:
            return request.user.uid == request.kwargs["pk"]