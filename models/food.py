from sqlmodel import SQLModel, Field
from typing import Optional

class FoodItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    source: str
    barcode: Optional[str] = Field(default=None, index=True)
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    sugar: float
    serving_size: str

class DailyLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: str
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float

class Meal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    daily_log_id: int = Field(foreign_key="dailylog.id")
    food_item_id: Optional[int] = Field(default=None, foreign_key="fooditem.id")
    type: str
    amount_g: float
    image_url: Optional[str] = None
    status: str = "pending_ai_review"
