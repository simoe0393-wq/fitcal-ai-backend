import pytest
from core.config import settings

def test_settings_loaded():
    assert settings.DATABASE_URL is not None
