from rest_framework import serializers

from accounts.serializers import ShortUserSerializer
from products.models import Category, Product, ProductPriceHistory


class ProductSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)

    class Meta:
        model = Product
        exclude = ()
        read_only_fields = ["author"]


class ProductShortSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ("id", "name")
        exclude = None


class CategorySerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)

    class Meta:
        model = Category
        exclude = ()
        read_only_fields = ["author"]


class ProductPriceHistorySerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()
    # task = ParseTaskSerializer()
    # parse_settings = SiteParseSettingsSerializer()

    class Meta:
        model = ProductPriceHistory
        exclude = ()


class StatusOkSerializer(serializers.Serializer):
    ok = serializers.BooleanField(default=True)


class StatusOkCountSerializer(serializers.Serializer):
    ok = serializers.BooleanField(default=True)
    count = serializers.IntegerField()
