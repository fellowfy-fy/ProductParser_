from rest_framework import serializers
from accounts.serializers import ShortUserSerializer

from products.models import Category, Product, ProductPriceHistory


class ProductSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer()

    class Meta:
        model = Product
        exclude = ()
        read_only_fields = ["author"]


class CategorySerializer(serializers.ModelSerializer):
    author = ShortUserSerializer()

    class Meta:
        model = Category
        exclude = ()
        read_only_fields = ["author"]


class ProductPriceHistorySerializer(serializers.ModelSerializer):
    author = ShortUserSerializer()

    class Meta:
        model = ProductPriceHistory
        exclude = ()
