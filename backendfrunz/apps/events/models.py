from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

from apps.core.models import TimeStampedModel


class Event(TimeStampedModel):
    class Format(models.TextChoices):
        OFFLINE = "offline", "Очно"
        ONLINE = "online", "Онлайн"
        MIXED = "mixed", "Смешанный формат"

    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"
        COMPLETED = "completed", "Завершено"
        CANCELLED = "cancelled", "Отменено"
        ARCHIVED = "archived", "Архив"

    title = models.CharField("Название", max_length=255)
    slug = models.SlugField("URL-адрес", max_length=255, unique=True, blank=True, allow_unicode=True)
    short_description = models.TextField("Краткое описание", max_length=500, blank=True)
    description = models.TextField("Описание")
    preview_image = models.ImageField("Превью", upload_to="events/previews/%Y/%m/", blank=True, null=True)
    start_datetime = models.DateTimeField("Дата и время начала")
    end_datetime = models.DateTimeField("Дата и время окончания", null=True, blank=True)
    location = models.ForeignKey(
        "core.Location",
        verbose_name="Площадка",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    format = models.CharField("Формат", max_length=20, choices=Format.choices, default=Format.OFFLINE)
    direction = models.ForeignKey(
        "core.Direction",
        verbose_name="Направление",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    age_min = models.PositiveIntegerField("Минимальный возраст", null=True, blank=True)
    age_max = models.PositiveIntegerField("Максимальный возраст", null=True, blank=True)
    organizer = models.CharField("Организатор", max_length=255, blank=True)
    registration_required = models.BooleanField("Нужна запись", default=True)
    registration_closed = models.BooleanField("Запись закрыта вручную", default=False)
    is_main = models.BooleanField("Показывать на главной", default=False)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ["start_datetime"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        indexes = [
            models.Index(fields=["status", "start_datetime"]),
            models.Index(fields=["is_main"]),
        ]

    @property
    def is_registration_available(self) -> bool:
        if not self.registration_required or self.registration_closed:
            return False
        if self.status != self.Status.PUBLISHED:
            return False
        return self.start_datetime >= timezone.now()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:event_detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title
