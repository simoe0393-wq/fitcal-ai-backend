import pytest
from unittest.mock import patch
from services.ai_service import get_coach_advice, get_personalized_coach_response
from schemas.ai import CoachChatRequest


# ── get_coach_advice (legacy locale-based) ─────────────────────────────────────

@pytest.mark.asyncio
async def test_coach_advice_mock_ar():
    with patch("core.config.settings.OPENROUTER_API_KEY", "mock"):
        advice = await get_coach_advice(locale="ar", daily_goal=2000, current_intake=1800)
        assert isinstance(advice, str)
        assert "Mock advice for ar" in advice


@pytest.mark.asyncio
async def test_coach_advice_mock_en():
    with patch("core.config.settings.OPENROUTER_API_KEY", "mock"):
        advice = await get_coach_advice(locale="en", daily_goal=2000, current_intake=1800)
        assert isinstance(advice, str)
        assert "Mock advice for en" in advice


# ── get_personalized_coach_response ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_personalized_response_low_protein():
    """Should flag LOW PROTEIN and return specific advice."""
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
        goal="lose",
    )
    with patch("core.config.settings.OPENROUTER_API_KEY", "mock"):
        response = await get_personalized_coach_response(request)
        assert isinstance(response, str)
        assert len(response) > 10
        # Mock mode returns protein-specific advice when LOW PROTEIN is flagged
        assert "protein" in response.lower()


@pytest.mark.asyncio
async def test_personalized_response_high_carbs():
    """Should flag HIGH CARBS when carbs exceed target."""
    request = CoachChatRequest(
        message="how am I doing?",
        calories_goal=2000,
        calories_consumed=1900,
        protein=130,
        protein_target=120,
        carbs=250,
        carbs_target=180,
        fat=55,
        fat_target=65,
        goal="lose",
    )
    with patch("core.config.settings.OPENROUTER_API_KEY", "mock"):
        response = await get_personalized_coach_response(request)
        assert isinstance(response, str)
        assert "carb" in response.lower()


@pytest.mark.asyncio
async def test_personalized_response_over_calories():
    """Should flag OVER CALORIES when consumed exceeds goal."""
    request = CoachChatRequest(
        message="check my intake",
        calories_goal=2000,
        calories_consumed=2400,
        protein=140,
        protein_target=120,
        carbs=160,
        carbs_target=180,
        fat=60,
        fat_target=65,
        goal="lose",
    )
    with patch("core.config.settings.OPENROUTER_API_KEY", "mock"):
        response = await get_personalized_coach_response(request)
        assert isinstance(response, str)
        assert "calorie" in response.lower() or "snack" in response.lower() or "dinner" in response.lower()


@pytest.mark.asyncio
async def test_personalized_response_all_good():
    """Should return optimisation tip when no alerts exist."""
    request = CoachChatRequest(
        message="hi",
        calories_goal=2200,
        calories_consumed=2000,
        protein=130,
        protein_target=120,
        carbs=170,
        carbs_target=180,
        fat=60,
        fat_target=70,
        goal="maintain",
    )
    with patch("core.config.settings.OPENROUTER_API_KEY", "mock"):
        response = await get_personalized_coach_response(request)
        assert isinstance(response, str)
        assert len(response) > 10


@pytest.mark.asyncio
async def test_personalized_response_no_nutrition_data():
    """Should not crash when optional nutrition fields are omitted."""
    request = CoachChatRequest(message="just chatting")
    with patch("core.config.settings.OPENROUTER_API_KEY", "mock"):
        response = await get_personalized_coach_response(request)
        assert isinstance(response, str)
        assert len(response) > 10
