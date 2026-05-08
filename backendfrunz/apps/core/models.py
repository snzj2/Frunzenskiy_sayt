from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        abstract = True


class PublishStatus(models.TextChoices):
    DRAFT = "draft", "Черновик"
    PUBLISHED = "published", "Опубликовано"
    ARCHIVED = "archived", "Архив"


class Direction(TimeStampedModel):
    title = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("URL-адрес", max_length=255, unique=True, blank=True, allow_unicode=True)
    description = models.TextField("Описание", blank=True)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Направление"
        verbose_name_plural = "Направления"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Location(TimeStampedModel):
    title = models.CharField("Название площадки", max_length=255)
    address = models.CharField("Адрес", max_length=500)
    latitude = models.DecimalField("Широта", max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField("Долгота", max_digits=9, decimal_places=6, null=True, blank=True)
    working_hours = models.TextField("Режим работы", blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    yandex_map_url = models.URLField("Ссылка на Яндекс.Карты", blank=True)
    is_active = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"

    def __str__(self) -> str:
        return self.title


class HomepageSettings(TimeStampedModel):
    title = models.CharField("Заголовок первого экрана", max_length=255)
    subtitle = models.TextField("Подзаголовок", blank=True)
    banner_image = models.ImageField("Изображение баннера", upload_to="homepage/banners/", blank=True, null=True)
    primary_button_text = models.CharField("Текст основной кнопки", max_length=100, blank=True)
    primary_button_url = models.CharField("Ссылка основной кнопки", max_length=255, blank=True)
    secondary_button_text = models.CharField("Текст второй кнопки", max_length=100, blank=True)
    secondary_button_url = models.CharField("Ссылка второй кнопки", max_length=255, blank=True)
    show_latest_news_count = models.PositiveSmallIntegerField("Количество новостей на главной", default=3)
    show_nearest_events_count = models.PositiveSmallIntegerField("Количество мероприятий на главной", default=3)
    show_clubs_count = models.PositiveSmallIntegerField("Количество клубов на главной", default=6)

    class Meta:
        verbose_name = "Настройки главной страницы"
        verbose_name_plural = "Настройки главной страницы"

    def __str__(self) -> str:
        return "Главная страница"


class DobroCenterPage(TimeStampedModel):
    title = models.CharField("Заголовок", max_length=255, default="Доброцентр")
    short_description = models.TextField("Краткое описание", blank=True)
    content = models.TextField("Текст страницы", blank=True)
    contact_person = models.CharField("Ответственный", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    is_published = models.BooleanField("Опубликовано", default=True)

    class Meta:
        verbose_name = "Страница Доброцентра"
        verbose_name_plural = "Страница Доброцентра"

    def __str__(self) -> str:
        return self.title


class DocumentCategory(TimeStampedModel):
    title = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("URL-адрес", max_length=255, unique=True, blank=True, allow_unicode=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Категория документов"
        verbose_name_plural = "Категории документов"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Document(TimeStampedModel):
    title = models.CharField("Название", max_length=255)
    category = models.ForeignKey(
        DocumentCategory,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
    )
    file = models.FileField("Файл", upload_to="documents/%Y/%m/")
    description = models.TextField("Описание", blank=True)
    status = models.CharField("Статус", max_length=20, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self) -> str:
        return self.title
