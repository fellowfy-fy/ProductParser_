from rest_framework import viewsets

from products.models import Category, Product, ProductPriceHistory
from products.serializers import CategorySerializer, ProductPriceHistorySerializer, ProductSerializer


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductPriceHistoryViewset(viewsets.ModelViewSet):
    serializer_class = ProductPriceHistorySerializer
    queryset = ProductPriceHistory.objects.all()
