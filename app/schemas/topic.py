from pydantic import BaseModel
from typing import Optional

class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicOut(TopicBase):
    id: int

    class Config:
        from_attributes = True