from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "start_datetime", "location", "format", "direction", "is_main", "registration_closed")
    list_filter = ("status", "format", "direction", "location", "is_main", "registration_closed")
    search_fields = ("title", "short_description", "description", "organizer")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_datetime"
    readonly_fields = ("created_at", "updated_at", "is_registration_available")
