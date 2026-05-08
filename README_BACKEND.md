# Backend Django для сайта ПМК «Фрунзенский»

В проект добавлена серверная часть на Django: настройки базы данных, модели, административная панель, первичные миграции, роли редакторов и простые JSON-endpoint'ы для будущей интеграции с frontend.

## Что добавлено

- `config/` — настройки Django-проекта.
- `apps/core/` — общие справочники: направления, площадки, документы, главная страница, Доброцентр.
- `apps/news/` — новости и галерея новостей.
- `apps/events/` — мероприятия.
- `apps/clubs/` — клубы и студии.
- `apps/applications/` — заявки на мероприятия, клубы и обратную связь.
- `apps/api/` — базовый публичный JSON API.
- `docker-compose.yml` — PostgreSQL для локального запуска.
- `.env.example` — пример переменных окружения.
- `requirements.txt` — зависимости Python.

## Быстрый запуск на SQLite

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Для SQLite временно уберите/закомментируйте POSTGRES_* в .env
python manage.py migrate
python manage.py createsuperuser
python manage.py setup_roles
python manage.py runserver
```

Админка будет доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

## Запуск на PostgreSQL через Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d db
python manage.py migrate
python manage.py createsuperuser
python manage.py setup_roles
python manage.py runserver
```

## Настройка базы данных

Django использует такую логику:

1. Если задан `DATABASE_URL`, используется он.
2. Если задан `POSTGRES_DB`, используется PostgreSQL через переменные `POSTGRES_*`.
3. Если переменные PostgreSQL не заданы, используется локальный SQLite-файл `db.sqlite3`.

Основные переменные:

```env
POSTGRES_DB=frunz_db
POSTGRES_USER=frunz_user
POSTGRES_PASSWORD=frunz_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

## Роли администраторов

Команда:

```bash
python manage.py setup_roles
```

создаёт группы:

1. `Админ: полный доступ` — все права на все модели.
2. `Редактор: мероприятия, новости, Доброцентр, главная` — мероприятия, новости, Доброцентр, главная, просмотр справочников.
3. `Редактор: клубы, студии, мероприятия, новости, главная` — клубы/студии, мероприятия, новости, главная, просмотр справочников.

После выполнения команды нужно зайти в `/admin/`, открыть пользователя и назначить ему нужную группу.

## Основные API endpoint'ы

```text
GET /api/health/
GET /api/news/
GET /api/events/
GET /api/clubs/
GET /api/locations/
```

Поддерживаемые фильтры:

```text
/api/news/?q=волонтерство
/api/events/?date_from=2026-05-01&direction=sport
/api/clubs/?direction=tvorchestvo&format=offline
```

## Следующий шаг

После настройки БД логично делать интеграцию frontend-страниц с backend: заменить статические карточки в HTML на данные из моделей `News`, `Event`, `Club`, `Location`.

## Обновление: красивая админ-панель и подключённый frontend

В этой версии добавлены:

- новая публичная главная страница Django по адресу `/`;
- динамические страницы `/news/`, `/events/`, `/clubs/`, `/documents/`, `/dobrocenter/`, `/contacts/`;
- карточки новостей, мероприятий и клубов подтягиваются из базы данных;
- формы записи на мероприятие и в клуб создают заявки в админке;
- форма обратной связи создаёт заявку типа «Обратная связь»;
- оформленная административная панель Django с новым dashboard, кнопкой «Открыть сайт» и современными стилями;
- команда `seed_demo` для тестового наполнения сайта.

### Как увидеть сайт и админку

```powershell
python manage.py migrate
python manage.py setup_roles
python manage.py seed_demo
python manage.py runserver
```

Публичный сайт:

```text
http://127.0.0.1:8000/
```

Админ-панель:

```text
http://127.0.0.1:8000/admin/
```

Если данных нет, страницы откроются с пустыми состояниями. Чтобы быстро увидеть карточки на сайте, выполните:

```powershell
python manage.py seed_demo
```

### Что редактируется из админки

- Главная страница: заголовок, подзаголовок, баннер, кнопки и количество карточек.
- Новости: публикация, превью, текст, галерея, признак вывода на главной.
- Мероприятия: дата, место, формат, направление, возраст, запись.
- Клубы и студии: описание, расписание, руководитель, контакты, адрес, формат.
- Заявки: заявки с публичного сайта появляются в разделе «Заявки».
- Доброцентр, документы, направления и площадки.


## Версия с исходным HTML

Фронтенд подключён из исходной папки `Frunz (1).zip`:

- стили: `static/frunz/style.css`;
- скрипты: `static/frunz/script.js`;
- иконки и иллюстрации: `static/frunz/assets/`;
- Django-шаблоны: `templates/site/`.

Сайт открывается по адресу `http://127.0.0.1:8000/`, админ-панель — `http://127.0.0.1:8000/admin/`.
Данные из админки выводятся на страницах `/`, `/news/`, `/events/`, `/clubs/`, `/documents/`, `/dobrocenter/`, `/contacts/`.
