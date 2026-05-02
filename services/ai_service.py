import json
import httpx
from core.config import settings
from schemas.ai import MealAnalysisResult

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-4o-mini"


# ── Shared OpenRouter helper ───────────────────────────────────────────────────

async def _call_openrouter(system_prompt: str, user_prompt: str) -> str:
    """
    Makes a POST request to OpenRouter and returns the AI text response.
    Raises on failure so callers can handle their own fallback.
    """
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"]
    if not content or not content.strip():
        raise ValueError("Empty response from OpenRouter")
    return content.strip()


# ── Meal image analysis (kept for compatibility, still uses vision approach) ───

async def analyze_meal_image(image_base64: str) -> MealAnalysisResult:
    """
    Analyzes a base64-encoded meal image.
    OpenRouter/gpt-4o-mini supports vision — falls back to mock if key not set.
    """
    if settings.OPENROUTER_API_KEY == "mock" or not settings.OPENROUTER_API_KEY:
        return MealAnalysisResult(
            food_name="Mock Salad",
            calories=350.0,
            carbs=20.0,
            protein=15.0,
            fat=10.0,
            confidence_score=0.95,
        )

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    system_prompt = (
        "You are a nutrition analysis assistant. "
        "Return ONLY a JSON object with exactly these fields: "
        "food_name (string), calories (number), carbs (number), "
        "protein (number), fat (number), confidence_score (number 0-1)."
    )
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this meal image and return the JSON."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            },
        ],
        "response_format": {"type": "json_object"},
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

        raw = data["choices"][0]["message"]["content"]
        parsed = json.loads(raw)

        # Robustness: flatten meal_components if returned
        if "meal_components" in parsed and "food_name" not in parsed:
            components = parsed["meal_components"]
            parsed["food_name"] = ", ".join(
                str(c.get("food_item", c.get("name", "Unknown"))) for c in components
            )
            parsed["calories"] = sum(float(c.get("calories", 0)) for c in components)
            parsed["carbs"] = sum(float(c.get("carbs", 0)) for c in components)
            parsed["protein"] = sum(float(c.get("protein", 0)) for c in components)
            parsed["fat"] = sum(float(c.get("fat", 0)) for c in components)
            parsed["confidence_score"] = parsed.get("confidence_score", 0.9)

        return MealAnalysisResult(**parsed)

    except Exception as e:
        raise Exception(f"AI analysis failed: {str(e)}")


# ── Legacy coach advice (locale-based, kept for GET /api/ai-coach) ─────────────

async def get_coach_advice(locale: str, daily_goal: int, current_intake: int) -> str:
    if settings.OPENROUTER_API_KEY == "mock" or not settings.OPENROUTER_API_KEY:
        return f"Mock advice for {locale}: Keep going!"

    system_prompt = "You are a helpful fitness coach. Be concise and motivating."
    user_prompt = (
        f"The user's locale is {locale}. "
        f"Their daily calorie goal is {daily_goal} kcal and they have consumed {current_intake} kcal. "
        "Give them one short, encouraging piece of advice in their language."
    )

    try:
        return await _call_openrouter(system_prompt, user_prompt)
    except Exception as e:
        return f"Encouraging words from your coach: You can do it! (Error: {str(e)})"


# ── Personalized AI coach (POST /api/ai-coach/chat) ───────────────────────────

async def get_personalized_coach_response(request) -> str:
    """
    Generates a personalized AI coach response based on real user nutrition data.
    Analyzes macros, flags issues (LOW PROTEIN, HIGH CARBS, OVER CALORIES),
    and builds a strict contextual prompt sent to OpenRouter.
    """
    # ── Macro analysis ─────────────────────────────────────────────────────
    flags = []
    macro_lines = []

    # Calories
    if request.calories_consumed is not None and request.calories_goal is not None:
        over = request.calories_consumed > request.calories_goal
        if over:
            flags.append("OVER CALORIES")
        macro_lines.append(
            f"- Calories: {request.calories_consumed}/{request.calories_goal} kcal"
            + (" (OVER CALORIES)" if over else "")
        )

    # Protein
    if request.protein is not None and request.protein_target is not None:
        low = request.protein < request.protein_target
        if low:
            flags.append("LOW PROTEIN")
        macro_lines.append(
            f"- Protein: {request.protein}/{request.protein_target}g"
            + (" (LOW PROTEIN)" if low else "")
        )

    # Carbs
    if request.carbs is not None and request.carbs_target is not None:
        high = request.carbs > request.carbs_target
        if high:
            flags.append("HIGH CARBS")
        macro_lines.append(
            f"- Carbs: {request.carbs}/{request.carbs_target}g"
            + (" (HIGH CARBS)" if high else "")
        )

    # Fat
    if request.fat is not None and request.fat_target is not None:
        macro_lines.append(f"- Fat: {request.fat}/{request.fat_target}g")

    # Goal label
    goal_label = {
        "lose": "lose weight",
        "gain": "gain muscle",
        "maintain": "maintain weight",
    }.get(request.goal or "", request.goal or "reach fitness goals")

    nutrition_block = "\n".join(macro_lines) if macro_lines else "No nutrition data provided."
    flags_block = ", ".join(flags) if flags else "No critical issues detected."

    # ── Prompt ─────────────────────────────────────────────────────────────
    system_prompt = "You are a strict professional fitness coach."

    user_prompt = (
        f"User nutrition data:\n{nutrition_block}\n"
        f"User goal: {goal_label}\n"
        f"Active alerts: {flags_block}\n\n"
        f"User message: {request.message}\n\n"
        "Rules:\n"
        "- MUST address at least one active alert if any exist\n"
        "- MUST give ONE specific, actionable recommendation\n"
        "- DO NOT use generic phrases like 'keep it up' or 'you're doing great'\n"
        "- MAX 2 sentences, be direct and professional\n"
        "- If no alerts, acknowledge good tracking and suggest one optimization\n\n"
        "Respond:"
    )

    print(f"[AI Coach] Active flags: {flags_block}")
    print(f"[AI Coach] Prompt:\n{user_prompt}")

    # ── Mock mode ──────────────────────────────────────────────────────────
    if settings.OPENROUTER_API_KEY == "mock" or not settings.OPENROUTER_API_KEY:
        if "LOW PROTEIN" in flags:
            return "Your protein intake is critically low — add a chicken breast or Greek yogurt to your next meal to hit your target."
        if "HIGH CARBS" in flags:
            return "Your carb intake exceeds your target — swap refined carbs for vegetables or legumes to stay on track."
        if "OVER CALORIES" in flags:
            return "You've exceeded your calorie goal — skip additional snacks and opt for a light, protein-rich dinner."
        return "Your macros are on track — consider timing your next meal around your workout for better performance."

    # ── Live OpenRouter call ───────────────────────────────────────────────
    try:
        return await _call_openrouter(system_prompt, user_prompt)
    except Exception as e:
        print(f"[AI Coach] OpenRouter error: {e}")
        return "Keep going, you're making progress!"
