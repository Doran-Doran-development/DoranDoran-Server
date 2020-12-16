from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.authentication import CustomJSONWebTokenAuthentication
from account.serializers import UserSerializer
from account.models import User

from .serializers import ReservationQueueSerializer
from .models import ReservationQueue
from .permissions import ReservePermission


class ReservationViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    serializer_class = ReservationQueueSerializer
    permission_classes = [IsAuthenticated, ReservePermission]
    queryset = ReservationQueue.objects.all()

    def create(self, request, *args, **kwargs):  # 학생만 가능
        serializer = ReservationQueueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance_user = User.objects.get(email=request.user.email)
        serializer.save(reserver_id=instance_user)

        return Response(serializer.data)

    # GET 요청은 모두 가능
    # DELETE 글 주인만 가능
    # POST 학생만 가능
    # PATCH 선생님만 가능