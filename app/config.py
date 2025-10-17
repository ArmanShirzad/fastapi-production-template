from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List, Optional
import secrets


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
    secret_key: str = ""  # Will be generated if empty
    cors_origins: List[str] = []  # Empty by default for security

    # Sentry
    sentry_dsn: Optional[str] = None

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Generate a random secret key if not provided
        if not self.secret_key:
            self.secret_key = secrets.token_urlsafe(32)

    model_config = ConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
