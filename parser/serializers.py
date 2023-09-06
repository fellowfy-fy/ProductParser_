from rest_framework import serializers

from parser.models import ParseTask, SiteParseSettings


class ParseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParseTask
        exclude = ()
        read_only_fields = ["author"]


class SiteParseSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteParseSettings
        exclude = ()
