import pytest
from core.config import settings

def test_all_settings_present():
    assert hasattr(settings, "DATABASE_URL")
    assert hasattr(settings, "MISTRAL_API_KEY")
    assert hasattr(settings, "USDA_API_KEY")
    assert hasattr(settings, "S3_BUCKET_NAME")
    assert hasattr(settings, "CLERK_SECRET_KEY")
