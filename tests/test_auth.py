import pytest
from core.auth import verify_token
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

@pytest.mark.asyncio
async def test_verify_token_missing():
    with pytest.raises(HTTPException) as exc_info:
        await verify_token(None)
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_verify_token_invalid():
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid")
    with pytest.raises(HTTPException) as exc_info:
        await verify_token(creds)
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_verify_token_valid():
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")
    clerk_id = await verify_token(creds)
    assert clerk_id == "mock_clerk_id"

