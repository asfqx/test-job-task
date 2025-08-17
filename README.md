# 🔎 Bank BIN Checker API

## 📌 Описание

Сервис для проверки **банковских карт по BIN-коду** (первые 6 цифр номера карты).  
С его помощью можно определить:
- банк-эмитент карты,
- его ID,
- валюту банка,
- корректность соответствия валюты карты и валюты банка.

### Логика работы:
1. Пользователь передаёт **номер карты** (`requisite`) и **валюту** (`currency`).
2. Сервис извлекает BIN (первые 6 цифр).
3. Проверяет данные:
   - в базе (`PostgreSQL`);
   - в кеше (`Redis`);
   - при необходимости обращается к внешнему API **apilayer/bincheck**;
   - справочник BIN может быть подгружен вручную с [bintable.com](https://bintable.com/country/ru?page=1).
4. Возвращает:
   - ✅ Успех — если валюта совпала с валютой банка;
   - ❌ Ошибку — если валюта или реквизиты не соответствуют.

---

## ⚙️ Используемые технологии

- **Python 3.11+**
- **FastAPI** — фреймворк для API.
- **SQLAlchemy (async)** — работа с PostgreSQL.
- **httpx** — асинхронные запросы к внешнему API.
- **Redis (aioredis)** — кэш BIN-кодов.
- **PostgreSQL** — основная база данных.
- **Pydantic** — схемы данных.
- **Uvicorn** — ASGI-сервер.
- **Docker + docker-compose** — контейнеризация и запуск окружения.

---

## 📂 Структура проекта

```
main.py
.env.example
requirements.txt
docker-compose.yml
Dockerfile
api/
 ├── config.py
 ├── db/
 │   ├── banks.json
 │   └── database.py
 ├── models/
 │   └── model.py
 ├── routes/
 │   ├── get_bank_from_api.py
 │   └── get_bank_from_bintable.py
 ├── schemas/
 │   └── method_names.py
 └── services/
     ├── dao.py
     ├── get_bank_from_api.py
     ├── get_bank_from_bintable.py
     ├── get_bank_from_db.py
     ├── get_bank_from_redis.py
     └── banks.py
```

---

## 🐳 Запуск через Docker

### 1. Подготовка
Создайте файл `.env` на основе `.env.example`:

```ini
# API Key для внешнего сервиса
API_KEY=<ваш_apilayer_api_key>

# PostgreSQL
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432
POSTGRES_DB_USER=postgres
POSTGRES_DB_PASS=postgres
POSTGRES_DB_NAME=testdb

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

### 2. Сборка и запуск контейнеров
```bash
docker-compose up --build
```

### 3. Доступ
- API → [http://localhost:8000](http://localhost:8000)
- PostgreSQL → `localhost:${POSTGRES_DB_PORT}`
- Redis → `localhost:${REDIS_PORT}`

---

## 📡 API Endpoints

### Проверка через внешний API
```
GET /bank_api?requisite=<номер_карты>&currency=<валюта>
```

✅ Успех:
```json
{
  "success": true,
  "result": {
    "id": 1,
    "name": "Сбербанк",
    "currency": "RUB"
  }
}
```

❌ Ошибка:
```json
{
  "success": false,
  "result": {
    "requisite": "4276381234567890"
  },
  "detail": "Неверная валюта"
}
```

---

### Проверка через Redis + DB (без внешнего API)
```
GET /bank_bintable_redis?requisite=<номер_карты>&currency=<валюта>
```

---

## 🧰 Особенности

- Внешний API ограничен по числу запросов → можно использовать альтернативный способ.
- BIN-таблица может обновляться вручную помощником (например, с сайта bintable.com).

---