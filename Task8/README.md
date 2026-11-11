# Задача 20: Расписание транспорта

**Студент:** Лупач Д.А.

Остановки и ближайшие рейсы. User: найти остановку, смотреть ближайшие. Tech: формат времени, источник данных. OpenAPI: остановки, рейсы по остановке, рейс по id, поиск остановки.

## Документация
- [Руководство пользователя](docs/user.md)
- [Техническая документация](docs/tech.md)
- OpenAPI: `openapi.yaml`

## Как открыть и посмотреть спецификацию
Вариант 1
Swagger UI в Docker:
```bash
docker run -p 8081:8080 -e SWAGGER_JSON=/spec/openapi.yaml \
  -v "$(pwd)":/spec swaggerapi/swagger-ui
```

Откройте http://localhost:8081.


Вариант 2:
Онлайн вставить содержимое `openapi.yaml` на https://editor.swagger.io.
