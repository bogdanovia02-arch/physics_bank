from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Topic, Task
from app.routers import auth, topics, tasks, recommend

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Physics Task Bank")

app.include_router(auth.router)
app.include_router(topics.router)
app.include_router(tasks.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "Physics Task Bank API is running"}