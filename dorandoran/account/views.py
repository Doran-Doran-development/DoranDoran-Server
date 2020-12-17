from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
    UserSerializer,
    RefreshJSONWebTokenSerializer,
)
from .models import User


class RegistrationView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = [AllowAny]


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


class SignOutView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        current_user = User.objects.get(email=request.user.email)
        current_user.delete()
        return Response(status=200)


class RefreshJSONWebTokenView(generics.GenericAPIView):
    serializer_class = RefreshJSONWebTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # serializer화 시키고
        if not serializer.is_valid():  # is_valid로 확인 하고
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data  # serializer_data 받아서 리턴
        return Response(
            {"success": True, "token": token},
            status=status.HTTP_200_OK,
        )