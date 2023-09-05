from django.contrib import admin

from parser.models import ParseTask

@admin.register(ParseTask)
class ParserTaskAdmin(admin.ModelAdmin):
    list_display = ("status", "author", "period", "work_mode", "created_at", "updated_at")
    list_filter = ("status", "author", "period")
    search_fields = ("urls",)
