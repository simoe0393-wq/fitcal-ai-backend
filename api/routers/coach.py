from fastapi import APIRouter, Depends
from core.auth import verify_token
from services.ai_service import get_coach_advice, get_personalized_coach_response
from schemas.ai import CoachChatRequest

router = APIRouter(prefix="/api/ai-coach", tags=["AI Coach"])


@router.get("")
async def get_coach(current_user=Depends(verify_token)):
    advice = await get_coach_advice("en", 2000, 1800)
    return {"advice": advice}


@router.post("/chat")
async def chat_with_coach(
    request: CoachChatRequest,
    current_user=Depends(verify_token),
):
    print("AI REQUEST DATA:", request.model_dump())
    response = await get_personalized_coach_response(request)
    return {"response": response}
