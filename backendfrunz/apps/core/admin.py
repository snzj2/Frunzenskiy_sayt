from django.contrib import admin

from .models import Direction, DobroCenterPage, Document, DocumentCategory, HomepageSettings, Location


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title", "address", "phone", "email", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "address", "phone", "email")


@admin.register(HomepageSettings)
class HomepageSettingsAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    fieldsets = (
        ("Первый экран", {"fields": ("title", "subtitle", "banner_image")}),
        ("Кнопки", {"fields": ("primary_button_text", "primary_button_url", "secondary_button_text", "secondary_button_url")}),
        ("Количество карточек", {"fields": ("show_latest_news_count", "show_nearest_events_count", "show_clubs_count")}),
    )


@admin.register(DobroCenterPage)
class DobroCenterPageAdmin(admin.ModelAdmin):
    list_display = ("title", "contact_person", "email", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "short_description", "content", "contact_person")


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published_at", "updated_at")
    list_filter = ("status", "category")
    search_fields = ("title", "description")
    date_hierarchy = "published_at"
