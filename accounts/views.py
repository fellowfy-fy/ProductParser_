import json
import logging

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import decorators, exceptions, permissions, response, viewsets

from accounts.models import CustomUser
from accounts.serializers import (
    CustomUserRegisterSerializer,
    CustomUserSelfEditSerializer,
    CustomUserSerializer,
)
from accounts.utils import get_user_role


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()


def email_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()

        return HttpResponseRedirect("/email_confirm?msg=Email Confirmed")
    else:
        logging.warning(f"Invalid email link! User: {user}")
        return HttpResponseRedirect("/email_error?msg=Invalid Link")


class CustomUserRegisterViewset(viewsets.ModelViewSet):
    serializer_class = CustomUserRegisterSerializer
    # permission_classes = [~permissions.IsAuthenticated]
    permission_classes: list[permissions.BasePermission] = []
    http_method_names = ["post"]

    def perform_create(self, serializer: CustomUserRegisterSerializer):
        assert isinstance(serializer.validated_data, dict)
        exists = CustomUser.objects.filter(email=serializer.validated_data["email"]).exists()
        if exists:
            raise exceptions.APIException(detail="User with this email already exists", code="user_exists")

        # invite_code_obj.delete()
        with transaction.atomic():

            # -- Pre registration
            user: CustomUser = serializer.save(
                email=serializer.validated_data["email"].lower(),
            )
            user.set_password(serializer.validated_data.get("password"))
            if not user.username:
                user.username = user.email
            user.save(update_fields=["password", "username"])

        # -- Post registration


class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ["username", "email", "first_name", "last_name", "middle_name"]
    filterset_fields = ["is_active", "role"]

    def get_queryset(self):
        if get_user_role(self.request.user) >= 3:
            return self.queryset
        return self.queryset.filter(id=self.request.user.pk)

    def get_object(self):
        pk = self.kwargs.get("pk")

        if pk in ["current", "me"] and self.request.user.is_authenticated:
            return self.request.user

        return super().get_object()

    @extend_schema(
        request=None,
        responses={200: CustomUserSerializer},
    )
    @decorators.action(["GET"], detail=False, permission_classes=[permissions.IsAuthenticated])
    def current(self, request):
        user = request.user

        return response.Response(CustomUserSelfEditSerializer(user).data)

    @decorators.action(["POST"], detail=True, permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request, pk=None):
        try:
            body = json.loads(request.body)
        except ValueError:
            raise exceptions.APIException("Invalid body", "invalid_body")
        try:
            if request.user.is_staff and pk not in ["current", "me"]:
                user = CustomUser.objects.get(pk=pk)
            else:
                user = request.user
        except CustomUser.DoesNotExist:
            raise exceptions.APIException("User not found", 404)

        password = body.get("password", "")
        if not password:
            raise exceptions.APIException("Empty password", "empty_password")
        user.set_password(password)
        user.save(update_fields=["password"])

        return response.Response({"ok": True})
