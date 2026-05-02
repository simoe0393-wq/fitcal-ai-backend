from fastapi import APIRouter, Depends
from core.auth import verify_token

router = APIRouter(prefix="/api", tags=["Progress"])

@router.post("/weight-progress", dependencies=[Depends(verify_token)])
async def log_weight(weight: float):
    return {"status": "success", "weight": weight}

@router.get("/weight-progress", dependencies=[Depends(verify_token)])
async def get_weight_progress():
    return {"history": []}

@router.post("/water", dependencies=[Depends(verify_token)])
async def log_water(amount_ml: int):
    return {"status": "success", "amount_ml": amount_ml}

@router.get("/water", dependencies=[Depends(verify_token)])
async def get_water():
    return {"total_ml": 0}
