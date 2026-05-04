from pydantic import BaseModel

class TaskBase(BaseModel):
    question: str
    answer: str
    difficulty: float = 3.0
    grade: int
    topic_id: int

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        from_attributes = True