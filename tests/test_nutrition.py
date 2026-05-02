import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from services.nutrition_service import get_food_by_barcode, search_usda

@pytest.mark.asyncio
async def test_get_food_by_barcode_real_mocked():
    # Mocking Open Food Facts response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Test Tuna",
            "nutriments": {
                "energy-kcal_100g": 110,
                "proteins_100g": 25,
                "carbohydrates_100g": 0,
                "fat_100g": 1
            },
            "serving_size": "100g"
        }
    }
    
    # We must patch the client inside the service
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        result = await get_food_by_barcode("123456789")
        assert result["name"] == "Test Tuna"
        assert result["calories"] == 110
        assert result["source"] == "OpenFoodFacts"

@pytest.mark.asyncio
async def test_search_usda_real_mocked():
    # Mocking USDA response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "foods": [
            {
                "description": "Raw Apple",
                "foodNutrients": [
                    {"nutrientName": "Energy", "value": 52},
                    {"nutrientName": "Protein", "value": 0.3}
                ]
            }
        ]
    }
    
    # Patch the settings in the service module
    with patch("services.nutrition_service.settings") as mock_settings:
        mock_settings.USDA_API_KEY = "real_key"
        mock_settings.OPEN_FOOD_FACTS_BASE_URL = "https://world.openfoodfacts.org"
        
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            result = await search_usda("Apple")
            assert result["name"] == "Raw Apple"
            assert result["calories"] == 52
            assert result["source"] == "USDA"

@pytest.mark.asyncio
async def test_nutrition_fallback():
    # Mocking API failure
    mock_response = MagicMock()
    mock_response.status_code = 500
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        result = await get_food_by_barcode("99999")
        assert result["source"] == "Fallback"
        assert result["name"] == "Unknown Product"
