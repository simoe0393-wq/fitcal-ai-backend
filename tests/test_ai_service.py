import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.ai_service import analyze_meal_image, get_coach_advice
from schemas.ai import MealAnalysisResult
from core.config import settings

@pytest.mark.asyncio
async def test_analyze_meal_mock_fallback():
    # Force mock mode
    with patch("core.config.settings.MISTRAL_API_KEY", "mock"):
        result = await analyze_meal_image("base64fake")
        assert isinstance(result, MealAnalysisResult)
        assert result.food_name == "Mock Salad"

@pytest.mark.asyncio
async def test_analyze_meal_valid_json():
    # Mock Mistral client
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"food_name": "Chicken", "calories": 200, "carbs": 0, "protein": 30, "fat": 8, "confidence_score": 0.9}'))
    ]
    
    with patch("core.config.settings.MISTRAL_API_KEY", "real_key"):
        # We need to mock the Mistral instance creation or the client methods
        with patch("services.ai_service.Mistral") as mock_mistral_class:
            mock_client = mock_mistral_class.return_value
            mock_client.chat.complete_async = AsyncMock(return_value=mock_response)
            
            result = await analyze_meal_image("base64fake")
            assert result.food_name == "Chicken"
            assert result.calories == 200.0

@pytest.mark.asyncio
async def test_analyze_meal_invalid_json():
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='invalid json'))
    ]
    
    with patch("core.config.settings.MISTRAL_API_KEY", "real_key"):
        with patch("services.ai_service.Mistral") as mock_mistral_class:
            mock_client = mock_mistral_class.return_value
            mock_client.chat.complete_async = AsyncMock(return_value=mock_response)
            
            with pytest.raises(Exception) as excinfo:
                await analyze_meal_image("base64fake")
            assert "AI analysis failed" in str(excinfo.value)

@pytest.mark.asyncio
async def test_get_coach_advice_mock():
    with patch("core.config.settings.MISTRAL_API_KEY", "mock"):
        advice = await get_coach_advice("ar", 2000, 1500)
        assert "Mock advice" in advice
