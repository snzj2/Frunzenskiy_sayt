# ПМК «Фрунзенский» — многостраничный frontend-макет

## Структура
- `index.html` — главная страница.
- `about.html` — о центре.
- `events.html` — мероприятия.
- `clubs.html` — клубы и студии.
- `news.html` — новости.
- `documents.html` — документы.
- `contacts.html` — контакты.
- `dobrocenter.html` — раздел Доброцентра.
- `accessibility.html` — доступная среда / версия для слабовидящих.
- `anticorruption.html` — противодействие коррупции.
- `style.css` — единая дизайн-система и адаптивная верстка.
- `script.js` — интерактив, фильтры, квиз, формы, доступность.

## Запуск
Откройте `index.html` в браузере или запустите локальный сервер:

```bash
python -m http.server 8000
```

и перейдите на `http://localhost:8000`.

---

## Backend

В проект добавлена Django-часть для базы данных и администрирования. Подробная инструкция: `README_BACKEND.md`.

Основной запуск backend:

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py setup_roles
python manage.py runserver
```
