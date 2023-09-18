from django.contrib import admin
from django.http.request import HttpRequest

from products.models import Category, Product, ProductPriceHistory


class ProductPriceHistoryInline(admin.TabularInline):
    model = ProductPriceHistory
    readonly_fields = ["task", "price", "created_at"]
    extra = 0
    can_delete = False

    def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "linked_id", "price", "created_at")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("name", "linked_id")
    filter_horizontal = ("categories",)
    inlines = [ProductPriceHistoryInline]


@admin.register(ProductPriceHistory)
class ProductPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "price", "created_at")
    list_filter = ("created_at",)
    autocomplete_fields = ("product",)
    readonly_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    readonly_fields = ("created_at", "updated_at")
