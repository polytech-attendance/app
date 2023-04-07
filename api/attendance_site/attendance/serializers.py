from rest_framework import serializers
from .models import Group
from .models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('group_id', 'groupname', 'groupleader_id')


class UserSerializer(serializers.Serializer):
    user_login = serializers.CharField(max_length=255)
    user_password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return User.objects.create(**validated_data)