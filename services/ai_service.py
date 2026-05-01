from schemas.ai import MealAnalysisResult

async def analyze_meal_image(base64_image: str) -> dict:
    return MealAnalysisResult(
        food_name="Apple",
        calories=95.0,
        carbs=25.0,
        protein=0.5,
        fat=0.3,
        confidence_score=0.98
    ).model_dump()

async def get_coach_advice(locale: str, calories: float, target: float) -> str:
    # MOCK implementation. System prompt uses `locale`
    if locale == "ar":
        return "رسالة المدرب الذكي باللغة العربية"
    return "Coach message"

