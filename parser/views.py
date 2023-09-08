import logging
from django.shortcuts import get_object_or_404
from accounts.models import RoleChoices
from parser.models import ParseTask, SiteParseSettings, TaskStatusChoices
from parser.serializers import ParseTaskSerializer, SiteParseSettingsSerializer, TestRunResultsSerializer
from parser.services.task_steps import change_task_status, check_task_steps

from computedfields.models import compute
from django.db.models import Q
from django_auto_prefetching import AutoPrefetchViewSetMixin
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter
from rest_framework import decorators, viewsets, fields, exceptions
from rest_framework.response import Response

from accounts.utils import get_user_role
from parser.tasks import run_now


class ParseTaskViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ParseTaskSerializer
    queryset = ParseTask.objects.all()

    def get_prefetchable_queryset(self):
        user = self.request.user
        role = get_user_role(user)
        if role == RoleChoices.ADMIN:
            return self.queryset
        elif role == RoleChoices.MANAGER:
            return self.queryset.filter(Q(author=user) | Q(author__manager=user))
        else:
            return self.queryset.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        compute(serializer.instance, "invalid_urls")
        check_task_steps(serializer.instance)

    @extend_schema(
        request=inline_serializer(
            "TaskChangeStatus", {"status": fields.ChoiceField(choices=TaskStatusChoices.choices)}
        ),
        responses={200: ParseTaskSerializer},
    )
    @decorators.action(["POST"], detail=True)
    def change_status(self, request, pk=None):
        task = get_object_or_404(ParseTask, pk=pk)

        status = request.data.get("status")
        change_task_status(task, status)
        return Response(ParseTaskSerializer(task).data)

    @extend_schema(request=None, responses={200: TestRunResultsSerializer}, parameters=[OpenApiParameter("test", bool)])
    @decorators.action(["POST"], detail=True)
    def test(self, request, pk=None):
        task = get_object_or_404(ParseTask, pk=pk)
        test = bool(request.GET.get("test"))

        task.log.clear()

        logging.info("Running test task...")
        bg_task = run_now(parse_task=task, test=test)
        logging.info(f"Waiting task: {bg_task}")
        try:
            res = bg_task(blocking=True)
        except Exception as e:
            logging.error("Test task failed", exc_info=e)
            raise exceptions.APIException(str(e))

        logging.info(f"Test task completed: {bg_task}")
        logging.debug(f"Test task completed. Result ({type(res)}): {res}")

        return Response(TestRunResultsSerializer(res).data)


class SiteParseSettingsViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = SiteParseSettingsSerializer
    queryset = SiteParseSettings.objects.all()
    search_fields = ["domain", "url", "url_match"]
    filterset_fields = ["parse_mode", "request_method", "force_parser_url"]

    def perform_update(self, serializer):
        return super().perform_update(serializer)
