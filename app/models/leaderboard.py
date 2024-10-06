from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class LeaderboardEntry(BaseModel):
    id: str = Field(default=None, alias="_id")
    user_id: str
    username: str
    score: int
    timestamp: datetime

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class LeaderboardResponse(BaseModel):
    category: str
    entries: List[LeaderboardEntry]

class GlobalLeaderboardResponse(BaseModel):
    time_period: str
    categories: List[LeaderboardResponse]