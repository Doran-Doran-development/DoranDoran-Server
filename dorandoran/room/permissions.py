from rest_framework import permissions


# is_teacher == true?
class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
<<<<<<< HEAD
        return bool(request.user.is_teacher)
=======

        return bool(request.user.role == 2)
>>>>>>> 022988459079668181a23f299d7fd1987ad08c70
