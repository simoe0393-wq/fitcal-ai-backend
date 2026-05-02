from PIL import Image
import io

import aioboto3
from core.config import settings

async def compress_image(image_bytes: bytes) -> bytes:
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")
    output = io.BytesIO()
    image.save(output, format="JPEG", quality=70, optimize=True)
    return output.getvalue()

async def upload_to_s3(filename: str, image_bytes: bytes) -> str:
    if settings.S3_ACCESS_KEY_ID == "mock" or not settings.S3_ACCESS_KEY_ID:
        return f"https://mock-cdn.com/{filename}"
    
    session = aioboto3.Session()
    async with session.client(
        's3',
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION
    ) as s3:
        await s3.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=filename,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
        # Construct public URL (or signed URL depending on policy)
        # Supabase S3 URL structure usually: {endpoint}/{bucket}/{key}
        return f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{filename}"

async def delete_from_s3(filename: str) -> bool:
    if settings.S3_ACCESS_KEY_ID == "mock" or not settings.S3_ACCESS_KEY_ID:
        return True
        
    session = aioboto3.Session()
    async with session.client(
        's3',
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION
    ) as s3:
        await s3.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=filename)
        return True

