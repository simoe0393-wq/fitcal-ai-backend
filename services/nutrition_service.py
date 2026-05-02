import httpx
from core.config import settings
from typing import Dict, Any, Optional

async def search_usda(query: str) -> Dict[str, Any]:
    """
    Search for food items using USDA FoodData Central.
    """
    if settings.USDA_API_KEY == "mock" or not settings.USDA_API_KEY:
        return {"name": f"Mock {query}", "source": "USDA", "calories": 95}
        
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={settings.USDA_API_KEY}&query={query}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                if data.get("foods"):
                    food = data["foods"][0]
                    # Map USDA nutrients (Simplified)
                    nutrients = {n["nutrientName"]: n["value"] for n in food.get("foodNutrients", [])}
                    return {
                        "name": food.get("description"),
                        "source": "USDA",
                        "calories": nutrients.get("Energy", 0),
                        "protein": nutrients.get("Protein", 0),
                        "carbs": nutrients.get("Carbohydrate, by difference", 0),
                        "fat": nutrients.get("Total lipid (fat)", 0),
                    }
        except Exception:
            pass
            
    return {"name": f"Mock {query}", "source": "USDA", "calories": 95}

async def get_food_by_barcode(barcode: str) -> Dict[str, Any]:
    """
    Lookup food items by barcode using Open Food Facts.
    """
    url = f"{settings.OPEN_FOOD_FACTS_BASE_URL}/api/v0/product/{barcode}.json"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 1:
                    product = data["product"]
                    nutriments = product.get("nutriments", {})
                    return {
                        "name": product.get("product_name", "Unknown Product"),
                        "barcode": barcode,
                        "source": "OpenFoodFacts",
                        "calories": nutriments.get("energy-kcal_100g", 0),
                        "protein": nutriments.get("proteins_100g", 0),
                        "carbs": nutriments.get("carbohydrates_100g", 0),
                        "fat": nutriments.get("fat_100g", 0),
                        "serving_size": product.get("serving_size", "100g")
                    }
        except Exception:
            pass
            
    return {
        "name": "Unknown Product",
        "barcode": barcode,
        "source": "Fallback",
        "calories": 0
    }
