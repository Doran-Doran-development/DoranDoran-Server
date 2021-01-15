from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from .serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
    UserSerializer,
    RefreshJSONWebTokenSerializer,
)
from .models import User
from .permissions import IsOwnerOrAdmin


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ("create", "list", "retrieve"):
            permission_classes = [AllowAny]
        elif self.action in ("destroy", "change_name", "change_password"):
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["patch"])
    def change_name(self, request, pk):
        current_user = self.get_object()
        current_user.name = request.data["new_name"]
        current_user.save()
        return Response("change_name")

    @action(detail=True, methods=["patch"])
    def change_password(self, request, pk):
        current_user = self.get_object()
        current_user.set_password(request.data["new_password"])
        current_user.save()
        return Response("change password")

    # POST - create user
    # GET - user get, list
    # DELETE - user delete
    # password 변경, 이름 변경 등은 따로 만들자


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # serializer화 시키고
        if not serializer.is_valid():  # is_valid로 확인 하고
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data  # serializer_data 받아서 리턴
        return Response(
            {"success": True, "token": token},
            status=status.HTTP_200_OK,
        )


class RefreshJSONWebTokenView(generics.GenericAPIView):
    serializer_class = RefreshJSONWebTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.headers)  # serializer화 시키고
        if not serializer.is_valid():  # is_valid로 확인 하고
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data  # serializer_data 받아서 리턴
        return Response(
            {"token": token},
            status=status.HTTP_200_OK,
        )
