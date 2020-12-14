from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_jwt import utils
from django.utils.translation import ugettext as _
import jwt
from django.contrib.auth.hashers import make_password


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'is_teacher')
    
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(data)  # backend.authenticate 쓰고
        if user is None:
            msg = _("User instance not exists")
            raise serializers.ValidationError(msg)

        payload = {
            "email" : user.email,
            "name" : user.name,
            "is_teacher" : user.is_teacher,
            "is_active" : user.is_active
        }
        token = utils.jwt_encode_handler(payload)  # token 만들고

        return user, token  # user, token 반환


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'is_teacher')
