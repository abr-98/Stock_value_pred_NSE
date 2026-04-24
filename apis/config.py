"""
API Configuration Settings
"""
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )
    
    # API Settings
    API_TITLE: str = "Stock Predictor API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for stock analysis, portfolio management, and market predictions"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # OpenAI (if needed)
    OPENAI_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None


# Global settings instance
settings = Settings()
