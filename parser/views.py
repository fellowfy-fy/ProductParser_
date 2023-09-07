from rest_framework import viewsets
from accounts.utils import get_user_role
from parser.models import ParseTask

from parser.serializers import ParseTaskSerializer
from django_auto_prefetching import AutoPrefetchViewSetMixin


class ParseTaskViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ParseTaskSerializer
    queryset = ParseTask.objects.all()

    def get_prefetchable_queryset(self):
        user = self.request.user
        role = get_user_role(user)
        if role == 3:
            return self.queryset
        # elif role == 2:
        #     return self.queryset.filter(author=user)
        else:
            return self.queryset.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
