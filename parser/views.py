from rest_framework import viewsets
from accounts.utils import get_user_role
from parser.models import ParseTask, SiteParseSettings

from parser.serializers import ParseTaskSerializer, SiteParseSettingsSerializer
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django.db.models import Q
from computedfields.models import compute


class ParseTaskViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ParseTaskSerializer
    queryset = ParseTask.objects.all()

    def get_prefetchable_queryset(self):
        user = self.request.user
        role = get_user_role(user)
        if role == 3:
            return self.queryset
        elif role == 2:
            return self.queryset.filter(Q(author=user) | Q(author__manager=user))
        else:
            return self.queryset.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        compute(serializer.instance, "invalid_urls")


class SiteParseSettingsViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = SiteParseSettingsSerializer
    queryset = SiteParseSettings.objects.all()
    search_fields = ["domain", "url", "url_match"]
    filterset_fields = ["parse_mode", "request_method", "force_parser_url"]

    def perform_update(self, serializer):
        return super().perform_update(serializer)
