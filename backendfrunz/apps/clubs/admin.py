from django.contrib import admin

from .models import Club


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "direction", "location", "format", "leader_name", "is_main")
    list_filter = ("status", "format", "direction", "location", "is_main")
    search_fields = ("title", "short_description", "description", "leader_name", "contact_phone", "contact_email")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("events",)
    readonly_fields = ("created_at", "updated_at")
