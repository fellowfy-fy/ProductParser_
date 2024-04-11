from parser.serializers import (
    ParseTaskShortSerializer,
    SiteParseSettingsShortSerializer,
)
from parser.services.excel_import import extract_import_products

from django_auto_prefetching import AutoPrefetchViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework import decorators, exceptions, parsers, viewsets
from rest_framework.response import Response

from products.models import Category, Product, ProductPriceHistory, StatusProduct
from products.serializers import (
    CategorySerializer,
    ProductPriceHistorySerializer,
    ProductSerializer,
    StatusOkCountSerializer,
    StatusProductSerializer,
)

class ProductViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by("-created_at").all()
    search_fields = ["name", "synonyms"]
    filterset_fields = ["author", "categories", "statusproducts"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        # request=inline_serializer(
        #     "ImportFile", {"file": fields.FileField}
        # ),
        request={
            "multipart/form-data": {"type": "object", "properties": {"file": {"type": "string", "format": "binary"}}},
        },
        responses={200: StatusOkCountSerializer},
    )
    @decorators.action(["POST"], detail=False)
    def import_products(self, request):
        contents = request.FILES.get("file")
        if not contents:
            raise exceptions.APIException("Файл не загружен")
        count = extract_import_products(contents.read(), author=request.user)

        return Response(StatusOkCountSerializer(dict(ok=True, count=count)).data)


class CategoryViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.order_by("-created_at").all()
    search_fields = ["name"]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance: Category):
        if instance.products.count() > 0:
            raise exceptions.APIException("У этого раздела есть продукты!")
        return super().perform_destroy(instance)
    
class StatusProductViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    serializer_class = StatusProductSerializer
    queryset = StatusProduct.objects.order_by("-created_at").all()
    search_fields = ["name"]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance: Category):
        if instance.products.count() > 0:
            raise exceptions.APIException("У этого статуса есть продукты!")
        return super().perform_destroy(instance)


class ProductPriceHistoryFullSerializer(ProductPriceHistorySerializer):
    parse_settings = SiteParseSettingsShortSerializer()
    task = ParseTaskShortSerializer()


class ProductPriceHistoryViewset(AutoPrefetchViewSetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductPriceHistoryFullSerializer
    queryset = ProductPriceHistory.objects.order_by("-created_at").all()

    filterset_fields = ["product", "task", "parse_settings", "product__statusproducts"]
