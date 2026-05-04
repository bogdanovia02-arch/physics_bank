from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
import random
from app import schemas, models, auth
from app.database import SessionLocal

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.post("/", response_model=List[schemas.TaskOut])
def recommend_tasks(request: schemas.RecommendRequest, db: Session = Depends(SessionLocal), current_user = Depends(auth.get_current_user)):
    query = db.query(models.Task)
    if request.topic_ids:
        query = query.filter(models.Task.topic_id.in_(request.topic_ids))
    if request.min_grade is not None:
        query = query.filter(models.Task.grade >= request.min_grade)
    if request.max_grade is not None:
        query = query.filter(models.Task.grade <= request.max_grade)
    if request.min_difficulty is not None:
        query = query.filter(models.Task.difficulty >= request.min_difficulty)
    if request.max_difficulty is not None:
        query = query.filter(models.Task.difficulty <= request.max_difficulty)
    tasks = query.all()
    if len(tasks) <= request.limit:
        result = tasks
    else:
        result = random.sample(tasks, request.limit)
    return result