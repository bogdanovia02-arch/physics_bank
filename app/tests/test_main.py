import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Используем отдельный файл для тестов
TEST_DB = "test_physics.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

# Создаём движок для тестовой БД
TEST_DATABASE_URL = f"sqlite:///{TEST_DB}"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Создаём таблицы в тестовой БД
Base.metadata.create_all(bind=test_engine)

# Переопределяем зависимость get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield

def create_test_user_and_token():
    unique = str(uuid.uuid4())[:8]
    username = f"user_{unique}"
    email = f"{username}@example.com"
    password = "secret"
    response = client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    assert response.status_code == 200, response.json()
    resp = client.post("/auth/login", data={"username": username, "password": password})
    assert resp.status_code == 200, resp.json()
    token = resp.json()["access_token"]
    return token

def auth_headers():
    token = create_test_user_and_token()
    return {"Authorization": f"Bearer {token}"}

def create_topic(headers, name="Механика"):
    response = client.post("/topics/", json={"name": name, "description": "Раздел физики"}, headers=headers)
    assert response.status_code == 201, response.json()
    return response.json()["id"]

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Physics Task Bank API is running"}

def test_register():
    response = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "alicepass"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    # Duplicate
    response = client.post("/auth/register", json={
        "username": "alice",
        "email": "bob@example.com",
        "password": "pass"
    })
    assert response.status_code == 400

def test_register_duplicate_email():
    response = client.post("/auth/register", json={
        "username": "alice",
        "email": "same@example.com",
        "password": "alicepass"
    })
    assert response.status_code == 200
    response = client.post("/auth/register", json={
        "username": "bob",
        "email": "same@example.com",
        "password": "bobpass"
    })
    assert response.status_code == 400

def test_login():
    client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "bobpass"
    })
    response = client.post("/auth/login", data={"username": "bob", "password": "bobpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    response = client.post("/auth/login", data={"username": "bob", "password": "wrong"})
    assert response.status_code == 401

def test_create_topic_unauthorized():
    response = client.post("/topics/", json={"name": "Механика", "description": "test"})
    assert response.status_code == 401

def test_crud_topics():
    headers = auth_headers()
    response = client.post("/topics/", json={"name": "Термодинамика", "description": "Законы"}, headers=headers)
    assert response.status_code == 201
    topic = response.json()
    assert topic["name"] == "Термодинамика"
    topic_id = topic["id"]
    response = client.get("/topics/")
    assert response.status_code == 200
    topics = response.json()
    assert len(topics) == 1
    assert topics[0]["id"] == topic_id
    response = client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Термодинамика"
    response = client.put(
        f"/topics/{topic_id}",
        json={"name": "Молекулярная физика", "description": "МКТ"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Молекулярная физика"
    response = client.delete(f"/topics/{topic_id}", headers=headers)
    assert response.status_code == 204
    response = client.get(f"/topics/{topic_id}")
    assert response.status_code == 404

def test_duplicate_topic_rejected():
    headers = auth_headers()
    response = client.post("/topics/", json={"name": "Оптика"}, headers=headers)
    assert response.status_code == 201
    response = client.post("/topics/", json={"name": "Оптика"}, headers=headers)
    assert response.status_code == 400

def test_update_topic_rejects_duplicate_name():
    headers = auth_headers()
    first_id = create_topic(headers, "Механика")
    second_id = create_topic(headers, "Оптика")
    response = client.put(
        f"/topics/{second_id}",
        json={"name": "Механика", "description": "duplicate"},
        headers=headers,
    )
    assert response.status_code == 400
    response = client.get(f"/topics/{first_id}")
    assert response.status_code == 200

def test_crud_tasks():
    headers = auth_headers()
    topic_id = create_topic(headers, "Оптика")
    task_data = {
        "question": "Скорость света?",
        "answer": "299792458",
        "difficulty": 1.0,
        "grade": 9,
        "topic_id": topic_id
    }
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 201
    task = response.json()
    task_id = task["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["answer"] == task_data["answer"]
    task_data["difficulty"] = 2.5
    response = client.put(f"/tasks/{task_id}", json=task_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["difficulty"] == 2.5
    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 204
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_task_validation_rejects_invalid_values():
    headers = auth_headers()
    topic_id = create_topic(headers, "Кинематика")
    response = client.post("/tasks/", json={
        "question": "v?",
        "answer": "",
        "difficulty": 6,
        "grade": 12,
        "topic_id": topic_id
    }, headers=headers)
    assert response.status_code == 422

def test_create_task_unknown_topic():
    headers = auth_headers()
    response = client.post("/tasks/", json={
        "question": "Найти ускорение тела",
        "answer": "a = F / m",
        "difficulty": 2,
        "grade": 9,
        "topic_id": 999
    }, headers=headers)
    assert response.status_code == 404

def test_recommend():
    headers = auth_headers()
    topic_id = create_topic(headers, "Электричество")
    tasks = [
        {"question": "question 1", "answer": "a1", "difficulty": 2, "grade": 10, "topic_id": topic_id},
        {"question": "question 2", "answer": "a2", "difficulty": 4, "grade": 11, "topic_id": topic_id},
        {"question": "question 3", "answer": "a3", "difficulty": 3, "grade": 9, "topic_id": topic_id},
    ]
    for t in tasks:
        resp = client.post("/tasks/", json=t, headers=headers)
        assert resp.status_code == 201
    payload = {
        "topic_ids": [topic_id],
        "min_grade": 9,
        "max_grade": 11,
        "min_difficulty": 2,
        "max_difficulty": 4,
        "limit": 2
    }
    response = client.post("/recommend/", json=payload, headers=headers)
    assert response.status_code == 200
    recs = response.json()
    assert len(recs) <= 2
    for rec in recs:
        assert rec["topic_id"] == topic_id

def test_recommend_requires_auth():
    response = client.post("/recommend/", json={"limit": 1})
    assert response.status_code == 401

def test_recommend_rejects_invalid_range():
    headers = auth_headers()
    response = client.post("/recommend/", json={
        "min_grade": 11,
        "max_grade": 9,
        "limit": 1
    }, headers=headers)
    assert response.status_code == 422
