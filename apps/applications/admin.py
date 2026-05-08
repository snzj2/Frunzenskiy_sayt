from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "application_type", "status", "event", "club", "phone", "email", "created_at")
    list_filter = ("application_type", "status", "created_at")
    search_fields = ("full_name", "phone", "email", "comment", "event__title", "club__title")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
