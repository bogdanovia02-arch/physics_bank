# Physics Task Bank API

REST API для банка задач по физике с JWT-авторизацией, CRUD-операциями и интеллектуальным подбором задач по теме, классу и сложности.

## Что реализовано

- регистрация и вход пользователей с выдачей JWT-токена;
- хранение пользователей, тем и задач в реляционной базе SQLite;
- CRUD для тем и задач;
- валидация входных данных через Pydantic;
- проверка связей между сущностями, например запрет создания задачи для несуществующей темы;
- подбор задач по фильтрам: тема, класс, сложность, лимит выдачи;
- автотесты ключевых сценариев через FastAPI TestClient;
- конфигурация pylint для проверки качества кода.

## Стек

- Python 3;
- FastAPI;
- SQLAlchemy;
- SQLite;
- Pydantic;
- python-jose и passlib для JWT и хеширования паролей;
- pytest;
- pylint.

## Структура проекта

```text
app/
  main.py              # точка входа FastAPI
  database.py          # подключение к базе данных
  auth.py              # JWT, пароли, текущий пользователь
  crud.py              # операции с БД
  models/              # SQLAlchemy-модели
  schemas/             # Pydantic-схемы
  routers/             # API-роутеры
  tests/               # автотесты
```

## Установка и запуск

```bash
git clone https://github.com/bogdanovia02-arch/physics_bank.git
cd physics_bank
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

При первом запуске SQLite-база `physics.db` создается автоматически.

## Основные эндпоинты

| Метод | URL | Описание | Авторизация |
| --- | --- | --- | --- |
| `GET` | `/` | Проверка работы API | нет |
| `POST` | `/auth/register` | Регистрация пользователя | нет |
| `POST` | `/auth/login` | Получение JWT-токена | нет |
| `GET` | `/topics/` | Список тем | нет |
| `POST` | `/topics/` | Создание темы | да |
| `GET` | `/topics/{topic_id}` | Получение темы | нет |
| `PUT` | `/topics/{topic_id}` | Обновление темы | да |
| `DELETE` | `/topics/{topic_id}` | Удаление темы | да |
| `GET` | `/tasks/` | Список задач | нет |
| `POST` | `/tasks/` | Создание задачи | да |
| `GET` | `/tasks/{task_id}` | Получение задачи | нет |
| `PUT` | `/tasks/{task_id}` | Обновление задачи | да |
| `DELETE` | `/tasks/{task_id}` | Удаление задачи | да |
| `POST` | `/recommend/` | Подбор задач по фильтрам | да |

## Примеры запросов

### Регистрация

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"student","email":"student@example.com","password":"pass1234"}'
```

### Логин

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student&password=pass1234"
```

В ответе будет `access_token`. Его нужно подставить в заголовок `Authorization`.

### Создание темы

```bash
curl -X POST http://127.0.0.1:8000/topics/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Механика","description":"Кинематика и динамика"}'
```

### Создание задачи

```bash
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"question":"Тело движется с ускорением 2 м/с^2. Найдите скорость через 5 с.","answer":"10 м/с","difficulty":2.0,"grade":9,"topic_id":1}'
```

### Подбор задач

```bash
curl -X POST http://127.0.0.1:8000/recommend/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"topic_ids":[1],"min_grade":9,"max_grade":11,"min_difficulty":1,"max_difficulty":3,"limit":3}'
```

## Тестирование и качество кода

```bash
pytest app/tests -v
pylint app --persistent=n
```

Текущее состояние локальной проверки:

- `13 passed`;
- `pylint 10.00/10`.

## Сценарий демонстрации

1. Открыть Swagger UI: http://127.0.0.1:8000/docs.
2. Показать структуру API и группы эндпоинтов.
3. Зарегистрировать пользователя через `/auth/register`.
4. Получить JWT через `/auth/login`.
5. Нажать `Authorize` в Swagger и вставить токен.
6. Создать тему, например `Механика`.
7. Создать несколько задач по этой теме.
8. Получить список задач и одну задачу по ID.
9. Показать подбор задач через `/recommend/`.
10. Кратко показать тесты и результат pylint.

## Автор

Илья Богданов, МФТИ, 2026.
