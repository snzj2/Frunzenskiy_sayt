from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.clubs.models import Club
from apps.core.models import Direction, DobroCenterPage, HomepageSettings, Location, PublishStatus
from apps.events.models import Event
from apps.news.models import News


class Command(BaseCommand):
    help = "Создаёт демонстрационные данные для проверки публичного сайта и админки."

    def handle(self, *args, **options):
        directions = {}
        for title in ["Творчество", "Спорт", "Добровольчество", "Медиа", "Патриотика"]:
            directions[title], _ = Direction.objects.get_or_create(title=title, defaults={"description": f"Направление: {title}"})

        location, _ = Location.objects.get_or_create(
            title="Главная площадка ПМК «Фрунзенский»",
            defaults={
                "address": "Санкт-Петербург, Фрунзенский район",
                "working_hours": "Пн–Пт 10:00–20:00",
                "phone": "+7 812 000-00-00",
                "email": "info@example.ru",
                "yandex_map_url": "https://yandex.ru/maps/2/saint-petersburg/",
            },
        )

        HomepageSettings.objects.get_or_create(
            title="Найди клуб, студию или мероприятие рядом с собой",
            defaults={
                "subtitle": "Актуальная афиша, новости и запись в активности подростково-молодёжного центра Фрунзенского района.",
                "primary_button_text": "Выбрать клуб",
                "primary_button_url": "/clubs/",
                "secondary_button_text": "Смотреть мероприятия",
                "secondary_button_url": "/events/",
            },
        )

        club_data = [
            ("Медиа-студия", "Медиа", "Фото, видео, монтаж и основы ведения социальных сетей."),
            ("Театральная лаборатория", "Творчество", "Актёрское мастерство, сценическая речь и постановки."),
            ("Волонтёрский штаб", "Добровольчество", "Подготовка и участие в добровольческих проектах района."),
        ]
        for title, direction, description in club_data:
            Club.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": description,
                    "description": description + " Занятия проходят в дружеской атмосфере под руководством наставника.",
                    "direction": directions[direction],
                    "location": location,
                    "format": Club.Format.OFFLINE,
                    "schedule": "Вт, Чт 16:00–18:00",
                    "age_min": 12,
                    "age_max": 18,
                    "leader_name": "Руководитель направления",
                    "is_main": True,
                    "status": Club.Status.ACTIVE,
                },
            )

        event_data = [
            ("Открытый мастер-класс по медиа", "Медиа", 3),
            ("Добровольческая акция района", "Добровольчество", 7),
            ("Творческий вечер молодёжи", "Творчество", 12),
        ]
        for title, direction, days in event_data:
            Event.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": "Анонс мероприятия для посетителей сайта.",
                    "description": "Подробное описание мероприятия, условия участия, место проведения и формат записи.",
                    "start_datetime": timezone.now() + timezone.timedelta(days=days),
                    "location": location,
                    "format": Event.Format.OFFLINE,
                    "direction": directions[direction],
                    "age_min": 12,
                    "age_max": 35,
                    "organizer": "ПМК «Фрунзенский»",
                    "is_main": True,
                    "status": Event.Status.PUBLISHED,
                },
            )

        for idx, title in enumerate(["Старт обновлённого сайта", "Набор в клубы и студии", "Итоги молодёжной акции"], start=1):
            News.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": "Краткий анонс новости на главной странице.",
                    "content": "Полный текст новости. Его можно заменить через красивую административную панель.",
                    "direction": directions["Творчество"],
                    "status": PublishStatus.PUBLISHED,
                    "is_main": True,
                    "published_at": timezone.now() - timezone.timedelta(days=idx),
                },
            )

        DobroCenterPage.objects.get_or_create(
            title="Доброцентр",
            defaults={
                "short_description": "Волонтёрские проекты и добровольческие возможности для молодёжи.",
                "content": "Здесь публикуется информация о волонтёрских акциях, направлениях помощи и контактах ответственных сотрудников.",
                "contact_person": "Координатор Доброцентра",
                "phone": "+7 812 000-00-01",
                "email": "dobro@example.ru",
            },
        )

        self.stdout.write(self.style.SUCCESS("Демонстрационные данные созданы. Откройте http://127.0.0.1:8000/"))
