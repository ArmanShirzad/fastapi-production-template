from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "FastAPI Template"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Database
    database_url: Optional[str] = None

    # Security
    secret_key: str = "your-secret-key-here"
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Sentry
    sentry_dsn: Optional[str] = None

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = ConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
