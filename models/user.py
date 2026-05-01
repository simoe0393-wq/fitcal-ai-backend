from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_id: str = Field(unique=True, index=True)
    email: str
    locale: str = "en"
    tier: str = "free"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Profile(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="user.id")
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    target_weight_kg: float
    activity_level: str
    goal: str
    daily_calorie_goal: int
    protein_goal: int
    carbs_goal: int
    fat_goal: int
