from rest_framework import serializers
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'is_teacher')
        extra_kwargs = {'password':{'writeonly':True}}
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)