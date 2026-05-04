from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(prefix="/topics", tags=["topics"])

@router.get("/", response_model=List[schemas.TopicOut])
def list_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_topics(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.TopicOut, status_code=status.HTTP_201_CREATED)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    return crud.create_topic(db=db, topic=topic)
