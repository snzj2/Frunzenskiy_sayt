# Generated manually for initial database setup.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("clubs", "0001_initial"),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255, verbose_name="ФИО")),
                ("phone", models.CharField(blank=True, max_length=50, verbose_name="Телефон")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("application_type", models.CharField(choices=[("event", "Запись на мероприятие"), ("club", "Запись в клуб / студию"), ("feedback", "Обратная связь")], max_length=20, verbose_name="Тип заявки")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                ("status", models.CharField(choices=[("new", "Новая"), ("in_progress", "В обработке"), ("approved", "Одобрена"), ("rejected", "Отклонена"), ("closed", "Закрыта")], default="new", max_length=20, verbose_name="Статус")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                ("club", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="applications", to="clubs.club", verbose_name="Клуб / студия")),
                ("event", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="applications", to="events.event", verbose_name="Мероприятие")),
            ],
            options={"verbose_name": "Заявка", "verbose_name_plural": "Заявки", "ordering": ["-created_at"]},
        ),
        migrations.AddIndex(model_name="application", index=models.Index(fields=["application_type", "status", "created_at"], name="applicatio_applica_fa0356_idx")),
    ]
