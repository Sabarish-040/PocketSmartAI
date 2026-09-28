from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    debug: bool = True
    database_url: str = "sqlite:///./pocketsmart.db"
    jwt_secret: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 120
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    max_upload_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()