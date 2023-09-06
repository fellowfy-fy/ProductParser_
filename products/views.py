from rest_framework import viewsets

from products.models import Category, Product, ProductPriceHistory
from products.serializers import CategorySerializer, ProductPriceHistorySerializer, ProductSerializer


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProductPriceHistoryViewset(viewsets.ModelViewSet):
    serializer_class = ProductPriceHistorySerializer
    queryset = ProductPriceHistory.objects.all()
