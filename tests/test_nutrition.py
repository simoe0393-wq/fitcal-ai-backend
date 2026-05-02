import pytest
from services.nutrition_service import get_food_by_barcode, search_usda

@pytest.mark.asyncio
async def test_get_food_by_barcode():
    result = await get_food_by_barcode("123456789")
    assert "name" in result
    assert result["barcode"] == "123456789"
    assert result["source"] == "OpenFoodFacts"

@pytest.mark.asyncio
async def test_search_usda():
    result = await search_usda("Apple")
    assert result["name"] == "Apple"
    assert result["source"] == "USDA"
