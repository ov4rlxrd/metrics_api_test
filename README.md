# Metrics API Test

REST-сервис на **FastAPI** для приема, хранения и анализа метрик устройств.

Сервис принимает показания устройства в формате:

```json
{
  "device_id": "dev-1",
  "x": 1.2,
  "y": 2.3,
  "z": 4.6
}
```

Данные сохраняются в **PostgreSQL**, после чего по `device_id` можно получить аналитику:
- минимальное значение
- максимальное значение
- количество
- сумму
- медиану

Аналитика рассчитывается отдельно для `x`, `y` и `z`.

---

## Стек

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- Docker Compose
- Locust

---

## Реализованный функционал

- прием метрик устройства
- хранение метрик в PostgreSQL
- получение аналитики по устройству
- фильтрация аналитики по временному периоду
- расчет агрегатов:
  - `min`
  - `max`
  - `count`
  - `sum`
  - `median`
- миграции БД через Alembic
- запуск проекта через Docker и Docker Compose
- нагрузочное тестирование через Locust

---

## Формат входных данных

Каждое устройство отправляет показания в формате:

```json
{
  "device_id": "dev-1",
  "x": 1.2,
  "y": 2.3,
  "z": 4.6
}
```

Каждая запись сохраняется в БД как отдельное измерение с временной меткой.


## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ov4rlxrd/metrics_api_test.git
cd metrics_api_test
```

### 2. Запустить проект

```bash
docker compose up --build
```

После запуска сервис будет доступен по адресу:

```text
http://localhost:8001
```

Swagger UI:

```text
http://localhost:8001/docs
```

## Конфигурация базы данных

PostgreSQL запускается в отдельном контейнере.

### Подключение внутри Docker-сети:
- host: `db`
- port: `5432`
- database: `metrics_db`

### Подключение с хоста:
- host: `localhost`
- port: `5433`
- database: `metrics_db`

---

## Миграции

Для миграций используется **Alembic**.

Если нужно применить миграции вручную:

```bash
docker compose exec app python -m alembic upgrade head
```

---

## API

### 1. Добавление метрик

```http
POST /metrics
```

#### Пример запроса

```json
{
  "device_id": "dev-1",
  "x": 1.2,
  "y": 2.3,
  "z": 4.6
}
```

#### Пример ответа

```json
{
  "id": 1,
  "device_id": "dev-1",
  "x": 1.2,
  "y": 2.3,
  "z": 4.6,
  "created_at": "2026-04-16T00:00:00"
}
```

---

### 2. Получение аналитики по устройству

```http
GET /metrics/{device_id}/analytics
```

#### Query-параметры
- `date_from` — начало периода
- `date_to` — конец периода

Если параметры не переданы, аналитика считается за все время.

#### Примеры запросов

```http
GET /metrics/dev-1/analytics
```

```http
GET /metrics/dev-1/analytics?date_from=2026-04-01T00:00:00&date_to=2026-04-16T00:00:00
```

#### Пример ответа

```json
{
  "device_id": "dev-1",
  "x": {
    "min": 0.9,
    "max": 1.4,
    "count": 3,
    "sum": 3.4,
    "median": 1.1
  },
  "y": {
    "min": 2.1,
    "max": 2.6,
    "count": 3,
    "sum": 6.9,
    "median": 2.2
  },
  "z": {
    "min": 3.1,
    "max": 3.8,
    "count": 3,
    "sum": 10.2,
    "median": 3.3
  }
}
```

## Пример сценария использования

1. Устройство отправляет метрики:
```json
{
  "device_id": "dev-1",
  "x": 1.0,
  "y": 2.0,
  "z": 3.0
}
```

2. Затем отправляет еще одно измерение:
```json
{
  "device_id": "dev-1",
  "x": 2.0,
  "y": 3.0,
  "z": 4.0
}
```

3. После этого можно запросить аналитику по `dev-1` и получить агрегированные значения по всем сохраненным измерениям.

---

## Нагрузочное тестирование

Нагрузочное тестирование выполнено с помощью **Locust**.

Тестировались два основных сценария:
- `POST /metrics`
- `GET /metrics/{device_id}/analytics`



![Locust Run 1](https://github.com/ov4rlxrd/metrics_api_test/blob/main/assets/locust_10_users.png)

![Locust Run 2](https://github.com/ov4rlxrd/metrics_api_test/blob/main/assets/locust_100_users.png)



## Репозиторий

GitHub:
`https://github.com/ov4rlxrd/metrics_api_test`
