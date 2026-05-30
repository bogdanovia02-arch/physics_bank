from pydantic import BaseModel, ConfigDict, Field

class TaskBase(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    answer: str = Field(min_length=1, max_length=1000)
    difficulty: float = Field(default=3.0, ge=1.0, le=5.0)
    grade: int = Field(ge=7, le=11)
    topic_id: int = Field(gt=0)

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
