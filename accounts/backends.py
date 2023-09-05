from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils import timezone
from drf_spectacular.authentication import SessionScheme
from rest_framework import pagination
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

UserModel = get_user_model()


class TotalPagesPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CsrfExemptSessionAuthenticationScheme(SessionScheme):
    target_class = "supervisor.serializers.CsrfExemptSessionAuthentication"


class CustomAuthorizationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = UserModel.objects.get(Q(email=username) | Q(username=username))
        except UserModel.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user


def is_token_expired(token):
    min_age = timezone.now() - timedelta(seconds=getattr(settings, "TOKEN_EXPIRED_AFTER_SECONDS", 60 * 60))
    expired = token.created < min_age
    return expired


class ExpiringTokenAuthentication(TokenAuthentication):
    """Same as in DRF, but also handle Token expiration.

    An expired Token will be removed and a new Token with a different
    key is created that the User can obtain by logging in with his
    credentials.

    Raise AuthenticationFailed as needed, which translates
    to a 401 status code automatically.
    https://stackoverflow.com/questions/14567586
    """

    keyword = "Bearer"

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted")

        expired = is_token_expired(token)
        if expired:
            token.delete()
            Token.objects.create(user=token.user)
            raise AuthenticationFailed("Token has expired")

        return (token.user, token)
