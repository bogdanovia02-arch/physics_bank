from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(prefix="/topics", tags=["topics"])

@router.get("/", response_model=List[schemas.TopicOut])
def list_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_topics(db, skip=skip, limit=limit)

@router.get("/{topic_id}", response_model=schemas.TopicOut)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = crud.get_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/", response_model=schemas.TopicOut, status_code=status.HTTP_201_CREATED)
def create_topic(
    topic: schemas.TopicCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    if crud.get_topic_by_name(db, topic.name):
        raise HTTPException(status_code=400, detail="Topic already exists")
    return crud.create_topic(db=db, topic=topic)

@router.put("/{topic_id}", response_model=schemas.TopicOut)
def update_topic(
    topic_id: int,
    topic_update: schemas.TopicCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    existing_topic = crud.get_topic_by_name(db, topic_update.name)
    if existing_topic and existing_topic.id != topic_id:
        raise HTTPException(status_code=400, detail="Topic already exists")
    topic = crud.update_topic(db, topic_id, topic_update)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    if not crud.delete_topic(db, topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")
