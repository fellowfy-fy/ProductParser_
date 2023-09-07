from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class RoleChoices(models.IntegerChoices):
    USER = 1, "Сотрудник"
    MANAGER = 2, "Руководитель"
    ADMIN = 3, "Администратор"


class CustomUser(AbstractUser):
    manager = models.ForeignKey("self", models.SET_NULL, null=True, blank=True, verbose_name=_("Руководитель"))
    middle_name = models.CharField(_("Отчество"), max_length=255, null=True, blank=True)
    role = models.PositiveSmallIntegerField(_("Роль"), choices=RoleChoices.choices, default=RoleChoices.USER)

    class Meta(AbstractUser.Meta):
        db_table = "auth_user"
        ordering = ("-date_joined",)

    def get_str(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name}".strip()

        return self.username
