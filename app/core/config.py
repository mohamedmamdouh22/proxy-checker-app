"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Proxy Checker API"
    app_version: str = "1.0.0"
    app_description: str = "FastAPI application for testing HTTP/HTTPS/SOCKS proxies"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Proxy Testing
    default_timeout: int = 10
    default_max_concurrent: int = 10
    test_url: str = "http://ip-api.com/json/"

    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
