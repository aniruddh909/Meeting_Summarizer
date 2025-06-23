from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv
from typing import ClassVar

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Meeting Assistant"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./meetings.db")
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 25 * 1024 * 1024  # 25MB
    ALLOWED_EXTENSIONS: set = {".mp3", ".wav", ".m4a"}

    # API Keys
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    HUGGINGFACE_API_KEY: str = HF_TOKEN  # For compatibility with summarizer
    
    # CORS
CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://meeting-assistant.vercel.app",
        "https://*.vercel.app"
    ]

class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 