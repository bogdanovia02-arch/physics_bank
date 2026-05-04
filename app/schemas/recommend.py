from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    topic_ids: Optional[List[int]] = None
    min_grade: Optional[int] = None
    max_grade: Optional[int] = None
    min_difficulty: Optional[float] = None
    max_difficulty: Optional[float] = None
    limit: int = 10