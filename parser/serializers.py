from rest_framework import serializers, fields
from accounts.serializers import ShortUserSerializer

from parser.models import MonitoringTypeChoices, NotificationTargetChoices, ParseTask, SiteParseSettings
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
