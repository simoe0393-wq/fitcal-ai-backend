from fastapi import Header, HTTPException

async def verify_token(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token = authorization.split(" ")[1]
    # In production, verify JWT using Clerk's JWKS. For now, mock it.
    if token == "invalid":
        raise HTTPException(status_code=401, detail="Invalid token")
    return "mock_clerk_id"
