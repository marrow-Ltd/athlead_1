"""
Centralized application settings.
Loaded from environment variables (.env in local dev, real env vars in prod).
NEVER hardcode secrets here — this file only defines names/defaults for non-sensitive values.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str

    # Auth
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS
    frontend_origin: str = "http://localhost:3000"

    # Cloudinary
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    # lru_cache -> settings are parsed once and reused (cheap + consistent across requests)
    return Settings()


settings = get_settings()
