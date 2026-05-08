# Generated manually for initial database setup.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True, verbose_name="URL-адрес", allow_unicode=True)),
                ("short_description", models.TextField(blank=True, max_length=500, verbose_name="Краткое описание")),
                ("description", models.TextField(verbose_name="Описание")),
                ("preview_image", models.ImageField(blank=True, null=True, upload_to="events/previews/%Y/%m/", verbose_name="Превью")),
                ("start_datetime", models.DateTimeField(verbose_name="Дата и время начала")),
                ("end_datetime", models.DateTimeField(blank=True, null=True, verbose_name="Дата и время окончания")),
                ("format", models.CharField(choices=[("offline", "Очно"), ("online", "Онлайн"), ("mixed", "Смешанный формат")], default="offline", max_length=20, verbose_name="Формат")),
                ("age_min", models.PositiveIntegerField(blank=True, null=True, verbose_name="Минимальный возраст")),
                ("age_max", models.PositiveIntegerField(blank=True, null=True, verbose_name="Максимальный возраст")),
                ("organizer", models.CharField(blank=True, max_length=255, verbose_name="Организатор")),
                ("registration_required", models.BooleanField(default=True, verbose_name="Нужна запись")),
                ("registration_closed", models.BooleanField(default=False, verbose_name="Запись закрыта вручную")),
                ("is_main", models.BooleanField(default=False, verbose_name="Показывать на главной")),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("published", "Опубликовано"), ("completed", "Завершено"), ("cancelled", "Отменено"), ("archived", "Архив")], default="draft", max_length=20, verbose_name="Статус")),
                ("direction", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="events", to="core.direction", verbose_name="Направление")),
                ("location", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="events", to="core.location", verbose_name="Площадка")),
            ],
            options={"verbose_name": "Мероприятие", "verbose_name_plural": "Мероприятия", "ordering": ["start_datetime"]},
        ),
        migrations.AddIndex(model_name="event", index=models.Index(fields=["status", "start_datetime"], name="events_even_status__3b5e5d_idx")),
        migrations.AddIndex(model_name="event", index=models.Index(fields=["is_main"], name="events_even_is_main_e0ad97_idx")),
    ]
