import pytest
from unittest.mock import patch
from services.ai_service import get_coach_advice

@pytest.mark.asyncio
async def test_coach_advice_mock():
    # Test with mock fallback
    with patch("core.config.settings.MISTRAL_API_KEY", "mock"):
        advice = await get_coach_advice(locale="ar", daily_goal=2000, current_intake=1800)
        assert isinstance(advice, str)
        assert "Mock advice for ar" in advice

@pytest.mark.asyncio
async def test_coach_advice_en_mock():
    with patch("core.config.settings.MISTRAL_API_KEY", "mock"):
        advice = await get_coach_advice(locale="en", daily_goal=2000, current_intake=1800)
        assert isinstance(advice, str)
        assert "Mock advice for en" in advice
