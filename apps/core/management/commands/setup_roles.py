from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


ROLE_CONFIG = {
    "Админ: полный доступ": {
        "all_permissions": True,
    },
    "Редактор: мероприятия, новости, Доброцентр, главная": {
        "models": {
            ("events", "event"): ["add", "change", "view"],
            ("news", "news"): ["add", "change", "view"],
            ("news", "newsimage"): ["add", "change", "delete", "view"],
            ("core", "dobrocenterpage"): ["add", "change", "view"],
            ("core", "homepagesettings"): ["add", "change", "view"],
            ("core", "direction"): ["view"],
            ("core", "location"): ["view"],
            ("applications", "application"): ["view", "change"],
        }
    },
    "Редактор: клубы, студии, мероприятия, новости, главная": {
        "models": {
            ("clubs", "club"): ["add", "change", "view"],
            ("events", "event"): ["add", "change", "view"],
            ("news", "news"): ["add", "change", "view"],
            ("news", "newsimage"): ["add", "change", "delete", "view"],
            ("core", "homepagesettings"): ["add", "change", "view"],
            ("core", "direction"): ["view"],
            ("core", "location"): ["view"],
            ("applications", "application"): ["view", "change"],
        }
    },
}


class Command(BaseCommand):
    help = "Создаёт группы администраторов и назначает права доступа."

    def handle(self, *args, **options):
        for group_name, config in ROLE_CONFIG.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()

            if config.get("all_permissions"):
                permissions = Permission.objects.all()
            else:
                permission_ids = []
                for (app_label, model), actions in config["models"].items():
                    codenames = [f"{action}_{model}" for action in actions]
                    permission_ids.extend(
                        Permission.objects.filter(
                            content_type__app_label=app_label,
                            content_type__model=model,
                            codename__in=codenames,
                        ).values_list("id", flat=True)
                    )
                permissions = Permission.objects.filter(id__in=permission_ids)

            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(f"Группа настроена: {group_name} ({permissions.count()} прав)"))

        self.stdout.write(self.style.SUCCESS("Готово. Назначьте пользователей в нужные группы через Django admin."))
