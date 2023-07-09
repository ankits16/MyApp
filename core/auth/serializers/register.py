from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User
from django.conf import settings

class RegisterSerializer(UserSerializer):
    """User resister serializer"""
    # make sure password is aleast 8 characters
    #no loger that 128 characters
    #cannot be read by the user
    password_min_length = 4 if settings.DEBUG else 8
    password = serializers.CharField(max_length=128, min_length=password_min_length, write_only=True, required=True)

    class Meta:
        model = User

        #all fields that can be included in resquest/response
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)