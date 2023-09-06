from rest_framework import serializers

from products.models import Category, Product, ProductPriceHistory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ()
        read_only_fields = ["author"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ()
        read_only_fields = ["author"]


class ProductPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPriceHistory
        exclude = ()
