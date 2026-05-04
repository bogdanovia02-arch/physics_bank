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
source venv/bin/activate  # на Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"username":"user1","email":"user1@ex.com","password":"pass"}'
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=user1&password=pass"
curl -X POST http://localhost:8000/topics/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"name":"Механика"}'
curl -X POST http://localhost:8000/recommend/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"topic_ids":[1],"limit":3}'
pytest app/tests/ -v
Author: Ilya Bogdanov, 2026

### Шаг 3. Добавьте файлы для контроля качества (если ещё нет)

```bash
# Создаём .pylintrc (если отсутствует)
cat > .pylintrc << 'EOF'
[MASTER]
ignore=venv, migrations, tests

[FORMAT]
max-line-length=120

[MESSAGES CONTROL]
disable=missing-docstring,
        invalid-name,
        too-few-public-methods,
        unused-argument,
        no-member,
        import-error,
        broad-except,
        fixme,
        duplicate-code,
        C0115,
        C0116,
        R0903,
        R0913,
        W0621,
        W0613,
        R0801
