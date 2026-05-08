from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

from apps.core.models import PublishStatus, TimeStampedModel


class News(TimeStampedModel):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("URL-адрес", max_length=255, unique=True, blank=True, allow_unicode=True)
    short_description = models.TextField("Анонс", max_length=500, blank=True)
    content = models.TextField("Текст новости")
    preview_image = models.ImageField("Превью", upload_to="news/previews/%Y/%m/", blank=True, null=True)
    direction = models.ForeignKey(
        "core.Direction",
        verbose_name="Направление",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_items",
    )
    status = models.CharField("Статус", max_length=20, choices=PublishStatus.choices, default=PublishStatus.DRAFT)
    is_main = models.BooleanField("Показывать на главной", default=False)
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["is_main"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.status == PublishStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:news_detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title


class NewsImage(models.Model):
    news = models.ForeignKey(News, verbose_name="Новость", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Изображение", upload_to="news/gallery/%Y/%m/")
    caption = models.CharField("Подпись", max_length=255, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Изображение новости"
        verbose_name_plural = "Галерея новости"

    def __str__(self) -> str:
        return f"{self.news}: {self.caption or self.image.name}"
