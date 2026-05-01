from pydantic import BaseModel

class MealAnalysisResult(BaseModel):
    food_name: str
    calories: float
    carbs: float
    protein: float
    fat: float
    confidence_score: float
