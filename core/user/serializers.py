from rest_framework import serializers
from core.user.models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        source='public_id',
        read_only=True,
        format='hex'
        )
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'created_on',
            'updated_on',
        ]
        read_only_fields = ['is_active']
    