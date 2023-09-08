from django.urls import path
from rest_framework import routers

from accounts.views import CustomUserViewset, GlobalPreferencesOverrideViewSet, email_activate

router = routers.DefaultRouter()

# router.register("auth/register", CustomUserRegisterViewset, basename="register")
router.register("users", CustomUserViewset, basename="users")
router.register("global", GlobalPreferencesOverrideViewSet, "global")

urlpatterns = [
    path("activate/<uidb64>/<token>", email_activate, name="activate"),
]
