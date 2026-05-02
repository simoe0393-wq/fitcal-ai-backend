from fastapi import APIRouter, Depends, UploadFile, File
from core.auth import verify_token
from services.ai_service import analyze_meal_image
from services.storage_service import compress_image, upload_to_s3
from schemas.ai import MealAnalysisResult

router = APIRouter(prefix="/api/meal", tags=["Meal"])

@router.post("/analyze-image", dependencies=[Depends(verify_token)])
async def analyze_image_endpoint(image: UploadFile = File(...)):
    # Read, compress, and analyze
    image_bytes = await image.read()
    compressed = await compress_image(image_bytes)
    url = await upload_to_s3(image.filename, compressed)
    
    # Mock analysis step
    # We use a dummy base64 string because the true integration expects base64
    analysis = await analyze_meal_image("mock_base64_string")
    
    return {"analysis": analysis, "image_url": url}

@router.post("/daily-log", dependencies=[Depends(verify_token)])
async def add_meal_to_log(food_name: str, calories: float):
    return {"status": "success", "meal": {"food_name": food_name, "calories": calories}}

