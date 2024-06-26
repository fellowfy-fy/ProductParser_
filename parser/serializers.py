from enum import Enum
from parser.models import MonitoringTypeChoices, NotificationTargetChoices, ParseTask, SiteParseSettings

from rest_framework import fields, serializers

from accounts.serializers import ShortUserSerializer
from products.models import Product
from products.serializers import ProductSerializer, ProductShortSerializer


class ExportEnum(Enum):
    CURRENT = "current"
    DYNAMICS = "dynamics"
    DIFFERENCES = "differences"
    VARIATIONS = "variations"
    COMPETITORS = "competitors"

    @classmethod
    def choices(cls):
        r = []
        for opt in cls:
            r.append((opt.value, opt.name))
        return r

    @classmethod
    def get(cls, name: str):
        for opt in cls:
            if opt.value == name:
                return opt


class SiteParseSettingsSerializer(serializers.ModelSerializer):
    # author = ShortUserSerializer(read_only=True)

    class Meta:
        model = SiteParseSettings
        exclude = ()


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


class ParseTaskShortSerializer(ParseTaskSerializer):
    class Meta(ParseTaskSerializer.Meta):
        fields = ("id", "name")
        exclude = None


class SiteParseSettingsShortSerializer(SiteParseSettingsSerializer):
    class Meta(SiteParseSettingsSerializer.Meta):
        fields = ("id", "domain")
        exclude = None


class ParseResultSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.FloatField()


class TestRunResultsDataSerializer(serializers.Serializer):
    parse_result = ParseResultSerializer(many=True)
    task = ParseTaskShortSerializer()
    settings = SiteParseSettingsShortSerializer()
    product = ProductShortSerializer(required=False)


class TestRunResultsLogSerializer(serializers.Serializer):
    level = serializers.CharField()
    message = serializers.CharField()
    time = serializers.CharField()
    exception = serializers.CharField(required=False)


class TestRunResultsSerializer(serializers.Serializer):
    data = TestRunResultsDataSerializer(many=True)
    logs = TestRunResultsLogSerializer(many=True)


class ExportRequestSerializer(serializers.Serializer):
    task = serializers.IntegerField(required=False)
    products = serializers.ListSerializer(child=serializers.IntegerField(required=False))
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    type = serializers.ChoiceField(ExportEnum.choices())


class ExportResultsSerializer(serializers.Serializer):
    ok = serializers.BooleanField(default=True)
    path = serializers.CharField()
