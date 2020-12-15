from rest_framework.permissions import BasePermission
from reserve.models import ReservationQueue


class ReservePermission(BasePermission):
    # GET 요청은 모두 가능
    # DELETE 글 주인만 가능
    # POST 학생만 가능
    # PATCH 선생님만 가능
    def has_permission(self, request, view):
        if request.user.role == 1:  # Admin 유저는 모든 사용권한을 가진다
            return True

        if view.action in ("list", "retrieve"):
            return True
        elif view.action == "post":  # 학생 일때 가능
            return request.user.role == 3
        elif view.action == "patch":  # 선생님 일때 가능
            return request.user.role == 2
        elif view.action == "delete":
            reserver_id = ReservationQueue.objects.get(
                reserve_id=request.parser_context["kwargs"]["reserve_id"]
            )
            print(reserver_id)
            return reserver_id
