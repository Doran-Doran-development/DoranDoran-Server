from rest_framework import generics
from .serializers import CreateUserSerializer, LoginUserSerializer
from .models import User


class RegistrationView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()