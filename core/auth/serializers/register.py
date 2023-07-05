from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User

class RegisterSerializer(UserSerializer):
    """User resister serializer"""
    # make sure password is aleast 8 characters
    #no loger that 128 characters
    #cannot be read by the user

    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User

        #all fields that can be included in resquest/response
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create(**validated_data)