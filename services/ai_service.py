import json
from typing import Optional
from mistralai.client import Mistral
from core.config import settings
from schemas.ai import MealAnalysisResult
from pydantic import ValidationError

async def analyze_meal_image(image_base64: str) -> MealAnalysisResult:
    """
    Analyzes a base64 encoded image using Mistral Vision model.
    """
    if settings.MISTRAL_API_KEY == "mock" or not settings.MISTRAL_API_KEY:
        return MealAnalysisResult(
            food_name="Mock Salad",
            calories=350.0,
            carbs=20.0,
            protein=15.0,
            fat=10.0,
            confidence_score=0.95
        )

    client = Mistral(api_key=settings.MISTRAL_API_KEY)
    
    prompt = (
        "Analyze the meal in this image. Return a JSON object with EXACTLY these fields: "
        "food_name (string), calories (number), carbs (number), protein (number), fat (number), "
        "and confidence_score (number between 0 and 1). "
        "Return ONLY the JSON object. Do not include nested fields or meal_components."
    )
    
    try:
        response = await client.chat.complete_async(
            model="pixtral-12b-2409",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")
            
        data = json.loads(content)
        
        # Robustness: if AI returns meal_components instead of flat structure
        if "meal_components" in data and "food_name" not in data:
            components = data["meal_components"]
            data["food_name"] = ", ".join([str(c.get("food_item", c.get("name", "Unknown"))) for c in components])
            data["calories"] = sum([float(c.get("calories", 0)) for c in components])
            data["carbs"] = sum([float(c.get("carbs", 0)) for c in components])
            data["protein"] = sum([float(c.get("protein", 0)) for c in components])
            data["fat"] = sum([float(c.get("fat", 0)) for c in components])
            data["confidence_score"] = data.get("confidence_score", 0.9)
            
        return MealAnalysisResult(**data)
        
    except (ValidationError, json.JSONDecodeError, ValueError, Exception) as e:
        # We can log the error here if needed
        raise Exception(f"AI analysis failed: {str(e)}")

async def get_coach_advice(locale: str, daily_goal: int, current_intake: int) -> str:
    if settings.MISTRAL_API_KEY == "mock" or not settings.MISTRAL_API_KEY:
        return f"Mock advice for {locale}: Keep going!"

    client = Mistral(api_key=settings.MISTRAL_API_KEY)
    
    prompt = (
        f"You are a helpful weight loss coach. The user is in {locale}. "
        f"Their daily goal is {daily_goal} kcal and they have consumed {current_intake} kcal so far. "
        "Give them a short, encouraging piece of advice in their language (e.g. if locale is ar, use Arabic)."
    )
    
    try:
        response = await client.chat.complete_async(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Encouraging words from your coach: You can do it! (Error: {str(e)})"
