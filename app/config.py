import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "AI Customer Support API"
    version: str = "1.0.0"
    groq_api_key: str
    environment: str = "production"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()