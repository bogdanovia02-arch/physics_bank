# Physics Task Bank API

REST API для банка задач по физике с авторизацией JWT и рекомендацией задач.

## Функциональность

- Регистрация и вход пользователей (JWT)
- Управление темами (разделами физики)
- CRUD операции с задачами
- Рекомендация задач по фильтрам (тема, класс, сложность)

## Установка и запуск

```bash
git clone https://github.com/bogdanovia02-arch/physics_bank.git
cd physics_bank
python3 -m venv venv
source venv/bin/activate   # для Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
После запуска откройте http://localhost:8000/docs для Swagger UI.
Примеры запросов

Регистрация
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user1@example.com","password":"pass"}'
Логин (получение токена)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1&password=pass"
Создание темы (требуется токен, замените <token>)
curl -X POST http://localhost:8000/topics/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Механика","description":"Кинематика, динамика"}'
Рекомендация задач
curl -X POST http://localhost:8000/recommend/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"topic_ids":[1],"min_grade":9,"max_grade":11,"limit":3}'
Тестирование
pytest app/tests/ -v
Автор

Илья Богданов, МФТИ, 2026
