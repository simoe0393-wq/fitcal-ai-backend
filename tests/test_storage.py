import pytest
from services.storage_service import compress_image, upload_to_s3, delete_from_s3
from PIL import Image
import io

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
async def test_upload_to_s3():
    url = await upload_to_s3("test.jpg", b"fake_bytes")
    assert url == "https://mock-cdn.com/test.jpg"

@pytest.mark.asyncio
async def test_delete_from_s3():
    result = await delete_from_s3("test.jpg")
    assert result is True
