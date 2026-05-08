from django.core.exceptions import ValidationError
from django.db import models


class Application(models.Model):
    class Type(models.TextChoices):
        EVENT = "event", "Запись на мероприятие"
        CLUB = "club", "Запись в клуб / студию"
        FEEDBACK = "feedback", "Обратная связь"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В обработке"
        APPROVED = "approved", "Одобрена"
        REJECTED = "rejected", "Отклонена"
        CLOSED = "closed", "Закрыта"

    full_name = models.CharField("ФИО", max_length=255)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    application_type = models.CharField("Тип заявки", max_length=20, choices=Type.choices)
    event = models.ForeignKey(
        "events.Event",
        verbose_name="Мероприятие",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
    )
    club = models.ForeignKey(
        "clubs.Club",
        verbose_name="Клуб / студия",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
    )
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField("Дата отправки", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        indexes = [models.Index(fields=["application_type", "status", "created_at"])]

    def clean(self):
        super().clean()
        if not self.phone and not self.email:
            raise ValidationError("Нужно указать телефон или email.")
        if self.application_type == self.Type.EVENT and not self.event:
            raise ValidationError("Для записи на мероприятие нужно выбрать мероприятие.")
        if self.application_type == self.Type.CLUB and not self.club:
            raise ValidationError("Для записи в клуб нужно выбрать клуб или студию.")
        if self.application_type == self.Type.FEEDBACK and (self.event or self.club):
            raise ValidationError("Обратная связь не должна быть привязана к клубу или мероприятию.")

    def __str__(self) -> str:
        return f"{self.full_name} — {self.get_application_type_display()}"
