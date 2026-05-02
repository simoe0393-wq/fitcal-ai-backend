from fastapi import APIRouter, Depends
from core.auth import verify_token
from services.nutrition_service import get_food_by_barcode

router = APIRouter(prefix="/api/food", tags=["Nutrition"])

@router.get("/barcode/{barcode}", dependencies=[Depends(verify_token)])
async def get_barcode(barcode: str):
    return await get_food_by_barcode(barcode)

from services.nutrition_service import search_usda
@router.get("/search", dependencies=[Depends(verify_token)])
async def search_food(query: str):
    return await search_usda(query)

