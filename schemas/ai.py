from pydantic import BaseModel
from typing import Optional

class MealAnalysisResult(BaseModel):
    food_name: str
    calories: float
    carbs: float
    protein: float
    fat: float
    confidence_score: float


class CoachChatRequest(BaseModel):
    message: str
    calories_goal: Optional[float] = None
    calories_consumed: Optional[float] = None
    protein: Optional[float] = None
    protein_target: Optional[float] = None
    carbs: Optional[float] = None
    carbs_target: Optional[float] = None
    fat: Optional[float] = None
    fat_target: Optional[float] = None
    goal: Optional[str] = None  # e.g. "lose", "gain", "maintain"
