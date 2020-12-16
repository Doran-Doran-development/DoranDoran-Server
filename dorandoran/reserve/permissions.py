from rest_framework.permissions import BasePermission
from .models import ReservationQueue


class ReservePermission(BasePermission):
    # GET 요청은 모두 가능
    # DELETE 글 주인만 가능
    # POST 학생만 가능
    # PATCH 선생님만 가능
    def has_permission(self, request, view):
        if request.user.role == 1:  # Admin 유저는 모든 사용권한을 가진다
            return True
        print(view.action)
        if view.action in ("list", "retrieve"):
            return True
        elif view.action == "post":  # 학생 일때 가능
            return request.user.role == 3
        elif view.action == "partial_update":  # 선생님 일때 가능
            return request.user.role == 2
        elif view.action == "destroy":  # 예약 주인 일때 가능
            selected_queue = ReservationQueue.objects.get(id=request.parser_context["kwargs"]["pk"])
            return request.user.email == str(selected_queue.reserver_id)
