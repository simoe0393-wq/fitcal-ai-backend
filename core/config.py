from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/db"
    CLERK_SECRET_KEY: str = "mock"
    CLERK_JWKS_URL: str = "mock"
    MISTRAL_API_KEY: str = "mock"
    USDA_API_KEY: str = "mock"
    OPEN_FOOD_FACTS_BASE_URL: str = "https://world.openfoodfacts.org"
    S3_ENDPOINT_URL: str = "mock"
    S3_ACCESS_KEY_ID: str = "mock"
    S3_SECRET_ACCESS_KEY: str = "mock"
    S3_BUCKET_NAME: str = "mock"
    S3_REGION: str = "mock"

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
