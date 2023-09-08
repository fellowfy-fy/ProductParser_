from rest_framework import permissions

from accounts.models import RoleChoices
from accounts.utils import get_user_role


class AdminOnlyPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return get_user_role(request.user) >= RoleChoices.ADMIN
