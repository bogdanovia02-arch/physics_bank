from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Topic, Task

# Создаём таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Physics Task Bank")

@app.get("/")
def root():
    return {"message": "Physics Task Bank API is running"}