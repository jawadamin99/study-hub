from rest_framework import serializers

from user_auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "profile_picture",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        request = self.context.get("request")
        if not request or not request.user.is_authenticated or request.user.role != User.Role.ADMIN:
            validated_data["role"] = User.Role.EMPLOYEE
        return User.objects.create_user(password=password, **validated_data)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        group = self.user.groups.first()
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['group'] = group.name if group else None
        return data
