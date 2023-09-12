from rest_framework import serializers

from accounts.serializers import ShortUserSerializer
from products.models import Category, Product, ProductPriceHistory


class CategorySerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)

    class Meta:
        model = Category
        exclude = ()
        read_only_fields = ["author"]


class CategoryShortSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = ("id", "name")
        exclude = None


class ProductSerializer(serializers.ModelSerializer):
    categories = CategoryShortSerializer(many=True, read_only=True)
    categories_write = serializers.PrimaryKeyRelatedField(
        source="categories", many=True, write_only=True, queryset=Category.objects.all()
    )
    author = ShortUserSerializer(read_only=True)

    class Meta:
        model = Product
        exclude = ()
        read_only_fields = ["author"]


class ProductShortSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ("id", "name")
        exclude = None


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
