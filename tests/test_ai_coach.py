import pytest
from unittest.mock import patch
from services.ai_service import get_coach_advice, get_personalized_coach_response
from schemas.ai import CoachChatRequest

@pytest.mark.asyncio
async def test_coach_advice_mock():
    # Test with mock fallback
    with patch("core.config.settings.GEMINI_API_KEY", "mock"):
        advice = await get_coach_advice(locale="ar", daily_goal=2000, current_intake=1800)
        assert isinstance(advice, str)
        assert "Mock advice for ar" in advice

@pytest.mark.asyncio
async def test_coach_advice_en_mock():
    with patch("core.config.settings.GEMINI_API_KEY", "mock"):
        advice = await get_coach_advice(locale="en", daily_goal=2000, current_intake=1800)
        assert isinstance(advice, str)
        assert "Mock advice for en" in advice

@pytest.mark.asyncio
async def test_personalized_coach_response_mock():
    request = CoachChatRequest(
        message="hi",
        calories_goal=2200,
        calories_consumed=1800,
        protein=80,
        protein_target=150,
        carbs=200,
        carbs_target=180,
        fat=60,
        fat_target=70,
        goal="lose"
    )
    with patch("core.config.settings.GEMINI_API_KEY", "mock"):
        response = await get_personalized_coach_response(request)
        assert response == "Keep going, you're making progress!"
