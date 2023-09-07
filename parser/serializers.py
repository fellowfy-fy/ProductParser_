from rest_framework import serializers, fields
from accounts.serializers import ShortUserSerializer

from parser.models import MonitoringTypeChoices, NotificationTargetChoices, ParseTask, SiteParseSettings


class ParseTaskSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer()
    monitoring_type = fields.MultipleChoiceField(choices=MonitoringTypeChoices.choices)
    notifications_target = fields.MultipleChoiceField(choices=NotificationTargetChoices.choices)

    class Meta:
        model = ParseTask
        exclude = ()
        read_only_fields = ["author", "status"]


class SiteParseSettingsSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer()

    class Meta:
        model = SiteParseSettings
        exclude = ()
