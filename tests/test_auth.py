import pytest
from core.auth import verify_token
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_verify_token_missing():
    with pytest.raises(HTTPException) as exc_info:
        await verify_token(None)
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_verify_token_invalid():
    with pytest.raises(HTTPException) as exc_info:
        await verify_token("Bearer invalid")
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_verify_token_valid():
    clerk_id = await verify_token("Bearer valid_token")
    assert clerk_id == "mock_clerk_id"
