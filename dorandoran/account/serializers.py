import jwt
import json

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password

from .models import User
from .utils import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("uuid", "active", "date_joined")
        extra_kwargs = {
            "role": {"required": False},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        user = authenticate(
            email=attrs.get("email"), password=attrs.get("password")
        )  # base.py에서 지정해주지 않았기 때문에 ModelBackend의 authenticate를 쓴다.
        if user is None:
            msg = _("User instance not exists")
            raise serializers.ValidationError(msg)

        payload = jwt_payload_handler(user)  # token에 쓸 payload 생성

        token = jwt_encode_handler(payload)  # token 생성

        return {"email": user.email, "token": token}  # token 반환


class RefreshJSONWebTokenSerializer(serializers.Serializer):
    Authorization = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        token = attrs["Authorization"].split()[1]
        payload = jwt_decode_handler(token)  # 입력받은 token으로 payload 획득
        user = User.objects.get_by_natural_key(payload[User.USERNAME_FIELD])

        orig_iat = payload["iat"]  # 토큰의 발행 시기 (issued at)

        if orig_iat:
            refresh_limit = settings.JWT_AUTH["JWT_REFRESH_EXPIRATION_DELTA"]

            if isinstance(refresh_limit, timedelta):
                refresh_limit = refresh_limit.days * 24 * 3600 + refresh_limit.seconds

            expiration_time = orig_iat + int(refresh_limit)
            now_time = timegm(datetime.utcnow().utctimetuple())

            if now_time > expiration_time:
                msg = _("Refresh has expired")
                raise serializers.ValidationError(msg)
        else:
            msg = _("iat field is required")
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload["iat"] = orig_iat
        return {"token": jwt_encode_handler(new_payload)}
