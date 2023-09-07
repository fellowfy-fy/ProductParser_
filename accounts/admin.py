from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser


def get_custom_user_fieldsets() -> list:
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1][1]["fields"] = list(fieldsets[1][1]["fields"])
    fieldsets[1][1]["fields"].insert(2, "middle_name")
    fieldsets[1][1]["fields"].extend(["role", "manager"])
    return fieldsets


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = list(UserAdmin.list_display) + ["role"]
    fieldsets = get_custom_user_fieldsets()
    filter_horizontal = list(UserAdmin.filter_horizontal) + []
    list_filter = list(UserAdmin.list_filter) + []
    ordering = ("-date_joined",)
