"""Application configuration from environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Connectinno Backend"
    debug: bool = False
    firebase_credentials_path: str = "./config/firebase-service-account.json"
    firebase_database_url: str = ""
    firebase_web_api_key: str = ""
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
