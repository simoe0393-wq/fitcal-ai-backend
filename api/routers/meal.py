from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from core.auth import verify_token
from services.ai_service import analyze_meal_image
from services.storage_service import compress_image, upload_to_s3
from schemas.ai import MealAnalysisResult
import base64


router = APIRouter(prefix="/api/meal", tags=["Meal"])

@router.post("/analyze-image", dependencies=[Depends(verify_token)])
async def analyze_image_endpoint(image: UploadFile = File(...)):
    try:
        # Read, compress, and analyze
        image_bytes = await image.read()
        compressed = await compress_image(image_bytes)
        
        # Re-enable real S3 upload
        url = await upload_to_s3(image.filename, compressed)
        
        # Convert compressed image to base64 for AI analysis
        image_base64 = base64.b64encode(compressed).decode("utf-8")
        
        # Perform real AI analysis
        analysis = await analyze_meal_image(image_base64)
        
        return {"analysis": analysis, "image_url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {str(e)}")





@router.post("/daily-log", dependencies=[Depends(verify_token)])
async def add_meal_to_log(food_name: str, calories: float):
    return {"status": "success", "meal": {"food_name": food_name, "calories": calories}}

