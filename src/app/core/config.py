"""
Application configuration settings.
"""
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "Python App"
    DEBUG: bool = False
    ENV: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 