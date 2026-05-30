from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

class RecommendRequest(BaseModel):
    topic_ids: Optional[List[int]] = None
    min_grade: Optional[int] = Field(default=None, ge=7, le=11)
    max_grade: Optional[int] = Field(default=None, ge=7, le=11)
    min_difficulty: Optional[float] = Field(default=None, ge=1.0, le=5.0)
    max_difficulty: Optional[float] = Field(default=None, ge=1.0, le=5.0)
    limit: int = Field(default=10, ge=1, le=50)

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.min_grade is not None and self.max_grade is not None:
            if self.min_grade > self.max_grade:
                raise ValueError("min_grade must be less than or equal to max_grade")
        if self.min_difficulty is not None and self.max_difficulty is not None:
            if self.min_difficulty > self.max_difficulty:
                raise ValueError("min_difficulty must be less than or equal to max_difficulty")
        return self
