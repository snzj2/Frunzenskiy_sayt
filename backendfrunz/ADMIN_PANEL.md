# Админ-панель

В этой версии вместо самодельного шаблона подключена готовая тема **django-jazzmin**.
Она строится поверх стандартной Django admin, поэтому права, пользователи и группы остаются прежними.

## После обновления проекта

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py setup_roles
python manage.py runserver
```

Админка:

```text
http://127.0.0.1:8000/admin/
```

Сайт:

```text
http://127.0.0.1:8000/
```

## Важно

Старые файлы кастомной админки сохранены в `templates/admin_disabled/`.
Они больше не участвуют в отображении, чтобы не ломать вёрстку.
