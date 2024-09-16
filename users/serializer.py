from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    isAdmin = serializers.BooleanField(source="is_staff", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "fullName", "isAdmin", "password")
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def get_fullName(self, obj):
        return f"{obj.first_name} {obj.last_name}"
