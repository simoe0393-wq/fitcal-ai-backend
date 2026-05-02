from typing import Dict, Any

async def search_usda(query: str) -> Dict[str, Any]:
    # Mock implementation
    return {"name": "Apple", "source": "USDA", "calories": 95}

async def get_food_by_barcode(barcode: str) -> Dict[str, Any]:
    # Hybrid implementation: Try USDA first, fallback to OpenFoodFacts (mocked for TDD)
    return {
        "name": "Mock Product",
        "barcode": barcode,
        "source": "OpenFoodFacts",
        "calories": 250,
        "protein": 10,
        "carbs": 30,
        "fat": 5,
        "fiber": 2,
        "sugar": 10,
        "serving_size": "100g"
    }
