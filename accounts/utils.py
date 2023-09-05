from django.contrib.auth.models import AbstractBaseUser

from accounts.models import RoleChoices


def get_user_role(user: AbstractBaseUser) -> RoleChoices:
    return user.role # noqa
