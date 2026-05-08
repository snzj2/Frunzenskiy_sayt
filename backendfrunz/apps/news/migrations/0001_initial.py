# Generated manually for initial database setup.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="News",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True, verbose_name="URL-адрес", allow_unicode=True)),
                ("short_description", models.TextField(blank=True, max_length=500, verbose_name="Анонс")),
                ("content", models.TextField(verbose_name="Текст новости")),
                ("preview_image", models.ImageField(blank=True, null=True, upload_to="news/previews/%Y/%m/", verbose_name="Превью")),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("published", "Опубликовано"), ("archived", "Архив")], default="draft", max_length=20, verbose_name="Статус")),
                ("is_main", models.BooleanField(default=False, verbose_name="Показывать на главной")),
                ("published_at", models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")),
                ("author", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="news_items", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("direction", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="news", to="core.direction", verbose_name="Направление")),
            ],
            options={"verbose_name": "Новость", "verbose_name_plural": "Новости", "ordering": ["-published_at", "-created_at"]},
        ),
        migrations.CreateModel(
            name="NewsImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="news/gallery/%Y/%m/", verbose_name="Изображение")),
                ("caption", models.CharField(blank=True, max_length=255, verbose_name="Подпись")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("news", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="news.news", verbose_name="Новость")),
            ],
            options={"verbose_name": "Изображение новости", "verbose_name_plural": "Галерея новости", "ordering": ["order", "id"]},
        ),
        migrations.AddIndex(model_name="news", index=models.Index(fields=["status", "published_at"], name="news_news_status__fb0e06_idx")),
        migrations.AddIndex(model_name="news", index=models.Index(fields=["is_main"], name="news_news_is_main_a2f7f1_idx")),
    ]
