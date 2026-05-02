import pytest
from services.storage_service import compress_image, upload_to_s3, delete_from_s3
from PIL import Image
import io
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_compress_image():
    img = Image.new('RGB', (100, 100))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    original_bytes = img_byte_arr.getvalue()
    result_bytes = await compress_image(original_bytes)
    
    assert isinstance(result_bytes, bytes)
    # The output format is forced to JPEG
    result_img = Image.open(io.BytesIO(result_bytes))
    assert result_img.format == "JPEG"

@pytest.mark.asyncio
async def test_upload_to_s3_fallback():
    with patch("core.config.settings.S3_ACCESS_KEY_ID", "mock"):
        url = await upload_to_s3("test.jpg", b"fake_bytes")
        assert url == "https://mock-cdn.com/test.jpg"

@pytest.mark.asyncio
async def test_upload_to_s3_real_logic():
    # Mock the aioboto3 session and client
    with patch("services.storage_service.aioboto3.Session") as mock_session_class:
        mock_session = mock_session_class.return_value
        mock_client = AsyncMock()
        # Mocking the async context manager: async with session.client(...) as s3
        mock_session.client.return_value.__aenter__.return_value = mock_client
        
        with patch("core.config.settings.S3_ACCESS_KEY_ID", "real_key"):
            with patch("core.config.settings.S3_ENDPOINT_URL", "https://supabase.co"):
                with patch("core.config.settings.S3_BUCKET_NAME", "bucket"):
                    url = await upload_to_s3("test.jpg", b"fake_bytes")
                    assert "https://supabase.co/bucket/test.jpg" in url
                    mock_client.put_object.assert_called_once()

@pytest.mark.asyncio
async def test_delete_from_s3_mocked():
    with patch("services.storage_service.aioboto3.Session") as mock_session_class:
        mock_session = mock_session_class.return_value
        mock_client = AsyncMock()
        mock_session.client.return_value.__aenter__.return_value = mock_client
        
        with patch("core.config.settings.S3_ACCESS_KEY_ID", "real_key"):
            result = await delete_from_s3("test.jpg")
            assert result is True
            mock_client.delete_object.assert_called_once()
