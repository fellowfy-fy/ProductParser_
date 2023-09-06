from django.contrib import admin

from parser.models import ParseTask, SiteParseSettings


@admin.register(ParseTask)
class ParserTaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "author",
        "period",
        "work_mode",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "author", "period")
    # raw_id_fields = ("products",)
    filter_horizontal = ("products",)
    search_fields = ("urls", "name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SiteParseSettings)
class SiteParseSettingsAdmin(admin.ModelAdmin):
    list_display = ("domain", "parse_mode", "request_method")
    list_filter = ("parse_mode", "request_method")
    search_fields = ("url",)
