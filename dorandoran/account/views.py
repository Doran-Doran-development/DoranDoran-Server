from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
    UserSerializer,
    RefreshJSONWebTokenSerializer,
)
from .models import User


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "email"
    lookup_url_kwarg = "pk"

    def create(self, request, *args, **kwargs):  # allow any
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):  # allow any
        user_instance = self.get_object()
        serializer = self.get_serializer(user_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):  # allow any
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):  # IsAdmin or IsMyself
        user_instance = self.get_object()
        user_instance.delete()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):  # IsAdmin or IsMyself
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST - create user
    # GET - user get, list
    # DELETE - user delete
    # PUT - user Info modify


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


class MyUserInfoView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user = User.objects.get(email=request.user.email)
        serializer = self.get_serializer(current_user)

        return Response(serializer.data, status=200)


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
        serializer = self.get_serializer(data=request.headers)  # serializer화 시키고
        if not serializer.is_valid():  # is_valid로 확인 하고
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data  # serializer_data 받아서 리턴
        return Response(
            {"token": token},
            status=status.HTTP_200_OK,
        )
