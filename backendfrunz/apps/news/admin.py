from django.contrib import admin

from .models import News, NewsImage


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "is_main", "direction", "author", "published_at", "updated_at")
    list_filter = ("status", "is_main", "direction")
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    inlines = [NewsImageInline]
    readonly_fields = ("created_at", "updated_at")
