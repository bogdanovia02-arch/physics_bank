from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class TopicBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

class TopicCreate(TopicBase):
    pass

class TopicOut(TopicBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
