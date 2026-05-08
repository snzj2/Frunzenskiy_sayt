from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from apps.core.models import TimeStampedModel


class Club(TimeStampedModel):
    class Format(models.TextChoices):
        OFFLINE = "offline", "Очно"
        ONLINE = "online", "Дистанционно"
        MIXED = "mixed", "Смешанный формат"

    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        TEMPORARILY_UNAVAILABLE = "temporarily_unavailable", "Временно недоступен"
        ARCHIVED = "archived", "Архив"

    title = models.CharField("Название", max_length=255)
    slug = models.SlugField("URL-адрес", max_length=255, unique=True, blank=True, allow_unicode=True)
    short_description = models.TextField("Краткое описание", max_length=500, blank=True)
    description = models.TextField("Описание")
    preview_image = models.ImageField("Превью", upload_to="clubs/previews/%Y/%m/", blank=True, null=True)
    direction = models.ForeignKey(
        "core.Direction",
        verbose_name="Направление",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clubs",
    )
    location = models.ForeignKey(
        "core.Location",
        verbose_name="Площадка",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clubs",
    )
    format = models.CharField("Формат", max_length=20, choices=Format.choices, default=Format.OFFLINE)
    schedule = models.TextField("Расписание", blank=True)
    age_min = models.PositiveIntegerField("Минимальный возраст", null=True, blank=True)
    age_max = models.PositiveIntegerField("Максимальный возраст", null=True, blank=True)
    leader_name = models.CharField("Руководитель", max_length=255, blank=True)
    contact_phone = models.CharField("Телефон", max_length=50, blank=True)
    contact_email = models.EmailField("Email", blank=True)
    is_main = models.BooleanField("Показывать на главной", default=False)
    status = models.CharField("Статус", max_length=40, choices=Status.choices, default=Status.ACTIVE)
    events = models.ManyToManyField("events.Event", verbose_name="Связанные мероприятия", blank=True, related_name="clubs")

    class Meta:
        ordering = ["title"]
        verbose_name = "Клуб / студия"
        verbose_name_plural = "Клубы и студии"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["is_main"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:club_detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title
