import json
import google.generativeai as genai
from core.config import settings
from schemas.ai import MealAnalysisResult, CoachChatRequest
from pydantic import ValidationError

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

async def analyze_meal_image(image_base64: str) -> MealAnalysisResult:
    """
    Analyzes a base64 encoded image using Gemini Vision model.
    """
    if settings.GEMINI_API_KEY == "mock" or not settings.GEMINI_API_KEY:
        return MealAnalysisResult(
            food_name="Mock Salad",
            calories=350.0,
            carbs=20.0,
            protein=15.0,
            fat=10.0,
            confidence_score=0.95
        )

    # Use gemini-1.5-flash for vision
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = (
        "Analyze the meal in this image. Return a JSON object with EXACTLY these fields: "
        "food_name (string), calories (number), carbs (number), protein (number), fat (number), "
        "and confidence_score (number between 0 and 1). "
        "Return ONLY the JSON object. Do not include markdown formatting or extra text."
    )
    
    try:
        # Prepare image data
        image_data = {
            'mime_type': 'image/jpeg',
            'data': image_base64
        }
        
        response = model.generate_content(
            [prompt, image_data],
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        content = response.text
        if not content:
            raise ValueError("Empty response from Gemini")
            
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
        
    except Exception as e:
        print(f"Gemini analysis error: {str(e)}")
        raise Exception(f"AI analysis failed: {str(e)}")

async def get_coach_advice(locale: str, daily_goal: int, current_intake: int) -> str:
    """Legacy endpoint for simple advice."""
    if settings.GEMINI_API_KEY == "mock" or not settings.GEMINI_API_KEY:
        return f"Mock advice for {locale}: Keep going!"

    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = (
        f"You are a helpful weight loss coach. The user is in {locale}. "
        f"Their daily goal is {daily_goal} kcal and they have consumed {current_intake} kcal so far. "
        "Give them a short, encouraging piece of advice in their language."
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Keep going, you're making progress!"

async def get_personalized_coach_response(request: CoachChatRequest) -> str:
    """
    Generates a personalized AI coach response based on real user nutrition data using Google Gemini.
    """
    # Logging request data
    print("AI REQUEST DATA:", request.model_dump())

    if settings.GEMINI_API_KEY == "mock" or not settings.GEMINI_API_KEY:
        return "Keep going, you're making progress!"

    # Analyze macro status
    flags = []
    if request.protein is not None and request.protein_target is not None:
        if request.protein < request.protein_target:
            flags.append("LOW PROTEIN")
    if request.carbs is not None and request.carbs_target is not None:
        if request.carbs > request.carbs_target:
            flags.append("HIGH CARBS")
    if request.calories_consumed is not None and request.calories_goal is not None:
        if request.calories_consumed > request.calories_goal:
            flags.append("OVER CALORIES")

    # Build prompt
    nutrition_info = f"""
User data:
- Calories: {request.calories_consumed or 0}/{request.calories_goal or 0}
- Protein: {request.protein or 0}/{request.protein_target or 0}g ({ 'LOW' if 'LOW PROTEIN' in flags else 'OK' })
- Carbs: {request.carbs or 0}/{request.carbs_target or 0}g ({ 'HIGH' if 'HIGH CARBS' in flags else 'OK' })
- Fat: {request.fat or 0}/{request.fat_target or 0}g
Goal: {request.goal or 'lose weight'}
"""
    
    system_instruction = "You are a strict professional fitness coach."
    
    prompt = f"""
{nutrition_info}

User message: {request.message}

Rules:
- MUST mention at least one macro issue (protein/carbs/fat) if any exist (Active flags: {', '.join(flags) if flags else 'None'})
- MUST give specific actionable advice
- DO NOT use generic phrases
- MAX 2 sentences
- Be direct and helpful

Respond:"""

    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(f"{system_instruction}\n\n{prompt}")
        
        text = response.text
        if not text:
            text = "Keep going, you're making progress!"
        
        # Logging response
        print("AI RESPONSE:", text)
        return text.strip()
        
    except Exception as e:
        print(f"Gemini coach error: {str(e)}")
        return "Keep going, you're making progress!"
