from PIL import Image
import io

async def compress_image(image_bytes: bytes) -> bytes:
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")
    output = io.BytesIO()
    image.save(output, format="JPEG", quality=70, optimize=True)
    return output.getvalue()

async def upload_to_s3(filename: str, image_bytes: bytes) -> str:
    # MOCK implementation until AWS keys are provided
    return f"https://mock-cdn.com/{filename}"
    
async def delete_from_s3(filename: str) -> bool:
    return True
