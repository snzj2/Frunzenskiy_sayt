# Generated manually for initial database setup.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Club",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True, verbose_name="URL-адрес", allow_unicode=True)),
                ("short_description", models.TextField(blank=True, max_length=500, verbose_name="Краткое описание")),
                ("description", models.TextField(verbose_name="Описание")),
                ("preview_image", models.ImageField(blank=True, null=True, upload_to="clubs/previews/%Y/%m/", verbose_name="Превью")),
                ("format", models.CharField(choices=[("offline", "Очно"), ("online", "Дистанционно"), ("mixed", "Смешанный формат")], default="offline", max_length=20, verbose_name="Формат")),
                ("schedule", models.TextField(blank=True, verbose_name="Расписание")),
                ("age_min", models.PositiveIntegerField(blank=True, null=True, verbose_name="Минимальный возраст")),
                ("age_max", models.PositiveIntegerField(blank=True, null=True, verbose_name="Максимальный возраст")),
                ("leader_name", models.CharField(blank=True, max_length=255, verbose_name="Руководитель")),
                ("contact_phone", models.CharField(blank=True, max_length=50, verbose_name="Телефон")),
                ("contact_email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("is_main", models.BooleanField(default=False, verbose_name="Показывать на главной")),
                ("status", models.CharField(choices=[("active", "Активен"), ("temporarily_unavailable", "Временно недоступен"), ("archived", "Архив")], default="active", max_length=40, verbose_name="Статус")),
                ("direction", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="clubs", to="core.direction", verbose_name="Направление")),
                ("events", models.ManyToManyField(blank=True, related_name="clubs", to="events.event", verbose_name="Связанные мероприятия")),
                ("location", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="clubs", to="core.location", verbose_name="Площадка")),
            ],
            options={"verbose_name": "Клуб / студия", "verbose_name_plural": "Клубы и студии", "ordering": ["title"]},
        ),
        migrations.AddIndex(model_name="club", index=models.Index(fields=["status"], name="clubs_club_status_2967b8_idx")),
        migrations.AddIndex(model_name="club", index=models.Index(fields=["is_main"], name="clubs_club_is_main_e253a5_idx")),
    ]
