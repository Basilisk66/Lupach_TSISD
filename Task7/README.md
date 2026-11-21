# Задача 20: 20. Расписание транспорта (остановки и рейсы)

**Студент:** Лупач Д.А.

API рейсов + PostgreSQL. Compose: `api` и `db`. Добавить рейс, ближайшие рейсы по остановке. README: схема сервисов (таблица или mermaid).

## Схема сервисов

```mermaid
flowchart LR
    U[Пользователь / curl] -->|localhost:8000| API[api: Flask :5000]
    API -->|db:5432, сеть backend| DB[(db: PostgreSQL)]
    DB --- V[(том pgdata)]
```

| Сервис | Образ | Порт | Назначение |
|--------|-------|------|-----------|
| `api` | собирается из `app/Dockerfile` (python:3.12-slim) | 8000 → 5000 | REST API |
| `db`  | postgres:16-alpine | не публикуется | хранение остановок и рейсов |

Оба сервиса в сети `backend`. Данные БД лежат в томе `pgdata`.

## Запуск

```bash
cp .env.example .env
docker compose up --build
```

## Проверка

```bash
# 1. Здоровье сервиса
curl http://localhost:8000/health

# 2. Список остановок
curl http://localhost:8000/stops

# 3. Добавить рейс (маршрут 99 на остановке 1 в 10:00)
curl -X POST http://localhost:8000/trips \
  -H "Content-Type: application/json" \
  -d '{"route_number": "99", "stop_id": 1, "departure_time": "10:00"}'

# 4. Ближайшие рейсы по остановке после 08:00 (3 штуки)
curl "http://localhost:8000/stops/1/next?after=08:00&limit=3"
```

Проверка сохранения данных: `docker compose down`, затем `docker compose up` —
добавленный рейс остался. Полный сброс: `docker compose down -v`.

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/health` | проверка работы |
| GET | `/stops` | все остановки |
| POST | `/stops` | добавить остановку `{"name": "..."}` |
| POST | `/trips` | добавить рейс |
| GET | `/stops/<id>/next?after=ЧЧ:ММ&limit=N` | ближайшие рейсы |