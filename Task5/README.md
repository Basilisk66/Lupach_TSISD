# Задача 20: Конфиг Docker Compose для учебной БД

**Студент:** Лупач Д.А.

`docker-compose.yml` (или аналог). Ветка `add-redis` добавляет сервис и меняет сеть/переменные; ветка `tune-postgres` правит те же фрагменты файла под другую конфигурацию Postgres. Разрешите конфликт compose-файла.

## Ход работы


### Структура репозитория
- docker-compose.yml — конфигурация Docker Compose с сервисами Postgres и Redis;
- .gitignore — исключает служебные файлы (*.log, .env);
- README.md — отчёт по лабе.
### Список веток
+ main - Основная ветка, итоговая согласованная версия конфига
+ add-redis - Добавляет сервис Redis, сеть study_net, меняет переменные Postgres
+ tune-postgres - Переводит Postgres на postgres:16-alpine, меняет пользователя, порт, параметры

### Сценарий конфликта
Обе ветки правили одни и те же строки сервиса postgres в `docker-compose.yml`:

**Начальное состояние (`main` до ветвления):**
```yaml
version: "4.9"

services:
  postgres:
    image: postgres:15
    container_name: study_db
    environment:
      POSTGRES_USER: den
      POSTGRES_PASSWORD: 778921
      POSTGRES_DB: study_db
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  pg_data:
```

Ветка add-redis — добавила Redis и сеть, изменила пароль и добавила POSTGRES_HOST:
```yaml
version: "4.9"

services:
  postgres:
    image: postgres:15
    container_name: study_db
    environment:
      POSTGRES_USER: den
      POSTGRES_PASSWORD: 123456
      POSTGRES_DB: study_db
      POSTGRES_HOST: postgres
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    networks:
      - study_net

  redis:
    image: redis:7-alpine
    container_name: study_cache
    ports:
      - "6379:6379"
    networks:
      - study_net

volumes:
  pg_data:

networks:
  study_net:
    driver: bridge
```


Ветка tune-postgres — сменила образ, пользователя, пароль  и добавила параметры запуска Postgres:
```yaml
version: "4.9"

services:
  postgres:
    image: postgres:16-alpine
    container_name: study_db
    environment:
      POSTGRES_USER: den
      POSTGRES_PASSWORD: 525266
      POSTGRES_DB: study_db
      POSTGRES_MAX_CONNECTIONS: "200"
    ports:
      - "5433:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    command: >
      postgres -c shared_buffers=256MB -c work_mem=16MB

volumes:
  pg_data:
```


При слиянии add-redis в main (после tune-postgres) Git не смог автоматически объединить изменения в строках image, POSTGRES_USER, POSTGRES_PASSWORD и окружающих — возник merge-конфликт:


### как разрешили

Решил путем того, что Обьединил обе конфигурации

От tune-postgres Postgres'а взял более новый образ и параметры из Postgres'а  (postgres:16-alpine, study_user, password, POSTGRES_MAX_CONNECTIONS=200, порт 5433:5432)

Из add-redis добавил Redis и сеть (сервис redis:7-alpine, сеть study_net)

POSTGRES_HOST=postgres — сохранил из add-redis, чтобы сервисы могли обращаться друг к другу по имени в общей сети

Итоговый docker-compose.yml получился таким

```yml
version: "4.9"

services:
  postgres:
    image: postgres:16-alpine
    container_name: study_db
    environment:
      POSTGRES_USER: den
      POSTGRES_PASSWORD: 525266
      POSTGRES_DB: study_db
      POSTGRES_MAX_CONNECTIONS: "200"
      POSTGRES_HOST: postgres
    ports:
      - "5433:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    command: >
      postgres -c shared_buffers=256MB -c work_mem=16MB
    networks:
      - study_net

  redis:
    image: redis:7-alpine
    container_name: study_cache
    ports:
      - "6379:6379"
    networks:
      - study_net

volumes:
  pg_data:

networks:
  study_net:
    driver: bridge
```

### Команды для remote
* git remote add origin https://github.com/Basilisk66/Docker_Compose_DB.git
--Добавляет удалённый репозиторий

* git remote -v            
--Проверка, что origin привязан правильно

* git push -u origin main
--Отправляет локальную ветку main в удалённый репозиторий origin

* git push origin add-redis
-- Отправляет локальную ветку add-redis на GitHub

* git push origin tune-postgres
-- Отправляет локальную ветку tune-postgres на GitHub

* git push origin main
-- Отправляет обновлённую main с merge-коммитом на GitHub

* git pull origin main
--Забирает изменения из origin/main и сливает с локальной main


### Ссылка на репозиторий
[Docker_Compose_DB](https://github.com/Basilisk66/Docker_Compose_DB)





Команды в bash, которыми я выполнил эту лабу 
```bash
mkdir docker-compose-db-lab
cd docker-compose-db-lab
git init
git branch -M main

git status
git add .
git commit -m "Initial commit: basic docker-compose with service postgres"

git remote add origin https://github.com/Basilisk66/Docker_Compose_DB.git
git remote -v
git push -u origin main

git checkout -b add-redis
git add docker-compose.yml
$ git commit -m "branch add-redis: add service Redis, network study_net, updated variables: password_DB"

git checkout main
git checkout -b tune-postgres
git add docker-compose.yml
git commit -m "tune-postgres: switch postgres:16-alpine, new variables and port 5433"

git checkout main
git merge tune-postgres
git merge add-redis
git status
cat docker-compose.yml
git add docker-compose.yml
git commit -m "merge: resolved conflict add-redis and tune-postgres, merge Postgres 16 and Redis"

git push origin add-redis
git push origin tune-postgres
git push origin main
git pull origin main
```