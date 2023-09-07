"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from parser.urls import router as parser_router

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from rest_framework.authtoken import views

from accounts.urls import router as accounts_router
from products.urls import router as products_router

router = routers.DefaultRouter()
router_include = [
    accounts_router,
    parser_router,
    products_router,
]

for sub_router in router_include:
    router.registry.extend(sub_router.registry)


urlpatterns = [
    path("admin/", admin.site.urls),
    ###
    path("", include("accounts.urls")),
    ###
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/token/", views.obtain_auth_token),
    # path("api/v1/auth/token/", CustomObtainAuthToken.as_view()),
    path("api/v1/auth/", include("rest_framework.urls")),
    #
    #
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]

if settings.DEBUGBAR:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
