# Playlists API

REST API для музыкальных подборок. Пользователи собирают плейлисты из треков каталога, ставят звёзды подборкам и смотрят рейтинг за последние семь дней.

**Стек:** Python 3.13 · Django 6 · Django REST Framework · PostgreSQL · Gunicorn · Docker · GitHub Actions

## Возможности

- Каталог треков с исполнителями, жанрами и обложками. Поиск по части названия без учёта регистра.
- Плейлисты с описанием, обложкой, автором и списком треков. Список плейлистов поддерживает пагинацию `limit` и `offset`.
- Звёзды и рейтинг. Повторный запрос на голосование снимает звезду, а в `/trending/` попадают до 16 плейлистов, отсортированных по числу звёзд за последние семь дней.
- Регистрация через Djoser, вход и обновление JWT через HttpOnly-куки, выход с удалением кук. Публичные профили содержат аватар, био и суммарное число звёзд на плейлистах пользователя.

## Устройство backend

`apps/app` содержит модели каталога, плейлистов и звёзд. Рейтинг вычисляется в базе через фильтрованный `Count` в Django ORM. DRF использует отдельные сериализаторы для списка, детальной выдачи и записи плейлистов.

`apps/users` отвечает за модель пользователя и профили, `apps/auth` — за JWT в куках. Маршруты API собраны в `apps/api`, схема OpenAPI генерируется через drf-spectacular.

## Локальный запуск

Понадобятся Python 3.13 и запущенный PostgreSQL. Для отдельной локальной базы можно использовать Docker.

```bash
docker run --name playlists-db -d -p 127.0.0.1:5432:5432 \
  -e POSTGRES_DB=playlists_db \
  -e POSTGRES_USER=playlists_user \
  -e POSTGRES_PASSWORD=playlists_local \
  postgres:18
```

В корне репозитория установите зависимости и запустите API. Для уже настроенной базы подставьте свои значения `DB_*`.

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export DB_NAME=playlists_db DB_USER=playlists_user DB_PASSWORD=playlists_local
export DB_HOST=127.0.0.1 DB_PORT=5432
export DEBUG=True ALLOWED_HOSTS=localhost,127.0.0.1

python manage.py migrate
python manage.py seed_genres
python manage.py seed_tracks
python manage.py runserver
```

Откройте [документацию API в ReDoc](http://127.0.0.1:8000/api/v1/redoc/) или [скачайте схему OpenAPI](http://127.0.0.1:8000/api/v1/schema/). Чтобы заполнить каталог подборками, создайте пользователя `akhmy` командой `python manage.py createsuperuser --username akhmy` и выполните `python manage.py seed_playlists`.

## Основные маршруты

Все пути в таблице указаны относительно `/api/v1/`.

| Метод и путь | Действие |
| --- | --- |
| `GET /tracks/?search=bohemian` | Поиск треков по названию. На демоданных найдёт `Bohemian Rhapsody` |
| `GET /playlists/?limit=16&offset=0` | Список плейлистов от новых к старым |
| `GET /playlists/{id}/` | Плейлист с описанием и треками |
| `POST /playlists/` | Создать плейлист от имени текущего пользователя |
| `GET /playlists/trending/` | Рейтинг плейлистов за последние семь дней |
| `PATCH /playlists/{id}/upvote/` | Поставить или снять звезду после входа |
| `GET /users/{username}/` | Публичный профиль |
| `POST /auth/users/` | Регистрация с полями `username`, `password` и `re_password` |
| `POST /auth/jwt/create/` | Вход по `username` и `password` |
| `POST /auth/jwt/refresh/` | Обновление токенов |
| `POST /auth/jwt/logout/` | Выход |

## Тесты и CI/CD

```bash
python -m pytest -q
```

Pytest использует SQLite в памяти через `config.test_settings`. Тесты проверяют модели, поиск треков, выдачу плейлистов и добавление и снятие звезды.

- [CI](.github/workflows/ci.yml) запускает Ruff, pip-audit, Bandit и pytest при пуше в `dev`.
- [CD Delivery](.github/workflows/cd-delivery.yml) собирает Docker-образ, сканирует его через Trivy, публикует в GHCR и запускает Newman и Locust с PostgreSQL в Docker Compose. При успешном завершении обоих заданий образ получает тег `latest`.
- [CD Deploy](.github/workflows/cd-deploy.yml) вызывает переиспользуемый workflow деплоя при пуше в `main`.

[Коллекция Postman](test/integration/postman-collection.json) и [сценарий Locust](test/load/locustfile.py) требуют обновления сценариев входа. API передаёт токены в куках, а сценарии пытаются прочитать `access` из тела ответа.
