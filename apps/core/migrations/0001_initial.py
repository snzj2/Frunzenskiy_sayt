# Generated manually for initial database setup.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Direction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True, verbose_name="URL-адрес", allow_unicode=True)),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активно")),
            ],
            options={"verbose_name": "Направление", "verbose_name_plural": "Направления", "ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, verbose_name="Название площадки")),
                ("address", models.CharField(max_length=500, verbose_name="Адрес")),
                ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name="Широта")),
                ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name="Долгота")),
                ("working_hours", models.TextField(blank=True, verbose_name="Режим работы")),
                ("phone", models.CharField(blank=True, max_length=50, verbose_name="Телефон")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("yandex_map_url", models.URLField(blank=True, verbose_name="Ссылка на Яндекс.Карты")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать на сайте")),
            ],
            options={"verbose_name": "Площадка", "verbose_name_plural": "Площадки", "ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="HomepageSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок первого экрана")),
                ("subtitle", models.TextField(blank=True, verbose_name="Подзаголовок")),
                ("banner_image", models.ImageField(blank=True, null=True, upload_to="homepage/banners/", verbose_name="Изображение баннера")),
                ("primary_button_text", models.CharField(blank=True, max_length=100, verbose_name="Текст основной кнопки")),
                ("primary_button_url", models.CharField(blank=True, max_length=255, verbose_name="Ссылка основной кнопки")),
                ("secondary_button_text", models.CharField(blank=True, max_length=100, verbose_name="Текст второй кнопки")),
                ("secondary_button_url", models.CharField(blank=True, max_length=255, verbose_name="Ссылка второй кнопки")),
                ("show_latest_news_count", models.PositiveSmallIntegerField(default=3, verbose_name="Количество новостей на главной")),
                ("show_nearest_events_count", models.PositiveSmallIntegerField(default=3, verbose_name="Количество мероприятий на главной")),
                ("show_clubs_count", models.PositiveSmallIntegerField(default=6, verbose_name="Количество клубов на главной")),
            ],
            options={"verbose_name": "Настройки главной страницы", "verbose_name_plural": "Настройки главной страницы"},
        ),
        migrations.CreateModel(
            name="DobroCenterPage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(default="Доброцентр", max_length=255, verbose_name="Заголовок")),
                ("short_description", models.TextField(blank=True, verbose_name="Краткое описание")),
                ("content", models.TextField(blank=True, verbose_name="Текст страницы")),
                ("contact_person", models.CharField(blank=True, max_length=255, verbose_name="Ответственный")),
                ("phone", models.CharField(blank=True, max_length=50, verbose_name="Телефон")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("is_published", models.BooleanField(default=True, verbose_name="Опубликовано")),
            ],
            options={"verbose_name": "Страница Доброцентра", "verbose_name_plural": "Страница Доброцентра"},
        ),
        migrations.CreateModel(
            name="DocumentCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True, verbose_name="URL-адрес", allow_unicode=True)),
            ],
            options={"verbose_name": "Категория документов", "verbose_name_plural": "Категории документов", "ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("file", models.FileField(upload_to="documents/%Y/%m/", verbose_name="Файл")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("published", "Опубликовано"), ("archived", "Архив")], default="published", max_length=20, verbose_name="Статус")),
                ("published_at", models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="documents", to="core.documentcategory", verbose_name="Категория")),
            ],
            options={"verbose_name": "Документ", "verbose_name_plural": "Документы", "ordering": ["-published_at", "-created_at"]},
        ),
    ]
