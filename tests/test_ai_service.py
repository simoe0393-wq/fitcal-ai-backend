import pytest
from services.ai_service import analyze_meal_image

@pytest.mark.asyncio
async def test_analyze_meal():
    result = await analyze_meal_image("base64fake")
    assert "calories" in result
    assert result["food_name"] == "Apple"
    assert result["calories"] == 95.0
