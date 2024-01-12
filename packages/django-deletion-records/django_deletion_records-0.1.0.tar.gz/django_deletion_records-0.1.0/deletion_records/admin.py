from django.contrib import admin

from deletion_records.models import DeletedRecord


@admin.register(DeletedRecord)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("table_name", "object_id", "deleted_at")
    list_filter = ("deleted_at", "table_name")
    date_hierarchy = "deleted_at"
    search_fields = ("object_id__exact",)
    ordering = ("-id",)
