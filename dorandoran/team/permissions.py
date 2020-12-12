from rest_framework import permissions

class isTeacherOrNotDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return bool(request.user.is_teacher)
        return True