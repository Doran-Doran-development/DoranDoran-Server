from rest_framework import viewsets, permissions
from rest_framework.response import Response
from account.authentication import CustomJSONWebTokenAuthentication
from .serializers import ReservationQueueSerializer
from .models import ReservationQueue
from account.models import User


class ReservationViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    serializer_class = ReservationQueueSerializer

    def create(self, request, *args, **kwargs):
        serializer = ReservationQueueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_user = User.objects.get(email=request.user.email)
        serializer.save(reserver_id=instance_user)
        print(serializer.validated_data)
        return Response(serializer.validated_data)

    # GET 요청은 모두 가능
    # DELETE 글 주인만 가능
    # POST 학생만 가능
    # PATCH 선생님만 가능