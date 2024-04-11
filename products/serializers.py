from rest_framework import serializers

from accounts.serializers import ShortUserSerializer
from products.models import Category, Product, ProductPriceHistory, StatusProduct


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

class StatusProductSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)

    class Meta:
        model = StatusProduct
        exclude = ()
        read_only_fields = ["author"]


class StatusProductShortSerializer(StatusProductSerializer):
    class Meta(StatusProductSerializer.Meta):
        fields = ("id", "name")
        exclude = None

class ProductSerializer(serializers.ModelSerializer):
    categories = CategoryShortSerializer(many=True, read_only=True)
    categories_write = serializers.PrimaryKeyRelatedField(
        source="categories", many=True, write_only=True, queryset=Category.objects.all()
    )
    statusproducts = StatusProductShortSerializer(many=True, read_only=True)
    statusproducts_write = serializers.PrimaryKeyRelatedField(
        source="statusproducts", many=True, write_only=True, queryset=StatusProduct.objects.all()
    )
    author = ShortUserSerializer(read_only=True)

    class Meta:
        model = Product
        exclude = ()
        read_only_fields = ["author"]


class ProductShortSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ("id", "name", "categories", "statusproducts")
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
