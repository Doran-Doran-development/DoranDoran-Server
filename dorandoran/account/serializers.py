from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_jwt import utils
import jwt

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_teacher')
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField()
    
    def validate(self, data):
        credentials = {
            "email" : data["email"],
            "password" : data["password"]
        }
        user = authenticate(**credentials) # backend.authenticate 쓰고

        payload = {
            "email" : user.email,
            "is_teacher" : user.is_teacher,
            "is_active" : user.is_active
        }
        token = utils.jwt_encode_handler(payload) # token 만들고
        
        return user,token # user, token 반환