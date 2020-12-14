from rest_framework import generics, status
from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer
from .models import User
from rest_framework.response import Response


class RegistrationView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # serializer화 시키고
        if not serializer.is_valid():  # is_valid로 확인 하고
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user, token = serializer.validated_data  # serializer_data 받아서 리턴
        return Response(
            {"user": UserSerializer(user).data, "token": token},
            status=status.HTTP_200_OK,
        )
