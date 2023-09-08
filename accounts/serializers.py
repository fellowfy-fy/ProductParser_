from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    invite_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "username",
            "email",
            "password",
            "token",
        ]

    def get_token(self, instance):
        token, created = Token.objects.get_or_create(user=instance)
        return token.key

    def create(self, validated_data):
        validated_data.pop("invite_code")
        return super().create(validated_data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = [
            "groups",
            "user_permissions",
            "is_superuser",
            "password",
        ]
        read_only_fields = ["last_login", "date_joined", "is_staff", "is_superuser"]


class CustomUserSelfEditSerializer(CustomUserSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        read_only_fields = CustomUserSerializer.Meta.read_only_fields + [
            "email",
        ]

    def get_auth_token(self, instance):
        if not instance.is_authenticated:
            return ""
        token, created = Token.objects.get_or_create(user=instance)
        return token.key


class ShortUserSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        exclude = None
        fields = ["username", "id", "first_name", "last_name", "middle_name", "manager"]
