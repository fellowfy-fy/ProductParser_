from dataclasses import dataclass
from rest_framework import serializers, fields
from accounts.serializers import ShortUserSerializer
from rest_framework_dataclasses.serializers import DataclassSerializer

from parser.models import MonitoringTypeChoices, NotificationTargetChoices, ParseTask, SiteParseSettings
from parser.services.log import CachedLog
from parser.services.parse import ProcessResult
from products.models import Product
from products.serializers import ProductSerializer


class ParseTaskSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    monitoring_type = fields.MultipleChoiceField(choices=MonitoringTypeChoices.choices)
    notifications_target = fields.MultipleChoiceField(choices=NotificationTargetChoices.choices)
    products = ProductSerializer(many=True, read_only=True)
    products_write = serializers.PrimaryKeyRelatedField(
        source="products", many=True, write_only=True, queryset=Product.objects.all()
    )

    class Meta:
        model = ParseTask
        exclude = ()
        read_only_fields = ["author", "status"]


class SiteParseSettingsSerializer(serializers.ModelSerializer):
    # author = ShortUserSerializer(read_only=True)

    class Meta:
        model = SiteParseSettings
        exclude = ()


@dataclass
class TestRunResultsData:
    logs: list[CachedLog]
    data: list[ProcessResult]


class TestRunResultsSerializer(DataclassSerializer):
    class Meta:
        dataclass = TestRunResultsData
