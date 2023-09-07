from rest_framework import viewsets, exceptions

from products.models import Category, Product, ProductPriceHistory
from products.serializers import CategorySerializer, ProductPriceHistorySerializer, ProductSerializer


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    search_fields = ["name", "synonyms"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    search_fields = ["name"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance: Category):
        if instance.products.count() > 0:
            raise exceptions.APIException("У этого раздела есть продукты!")
        return super().perform_destroy(instance)


class ProductPriceHistoryViewset(viewsets.ModelViewSet):
    serializer_class = ProductPriceHistorySerializer
    queryset = ProductPriceHistory.objects.all()
