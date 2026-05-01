import pytest
from services.ai_service import get_coach_advice

@pytest.mark.asyncio
async def test_coach_advice():
    advice = await get_coach_advice(locale="ar", calories=2000, target=1800)
    assert isinstance(advice, str)
    assert advice == "رسالة المدرب الذكي باللغة العربية"

@pytest.mark.asyncio
async def test_coach_advice_en():
    advice = await get_coach_advice(locale="en", calories=2000, target=1800)
    assert isinstance(advice, str)
    assert advice == "Coach message"
