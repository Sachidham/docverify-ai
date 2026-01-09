from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    # App
    APP_NAME: str = "DocVerify AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str  # anon key
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    # Google Gemini
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"

    # Anthropic (Claude)
    ANTHROPIC_API_KEY: Optional[str] = None

    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"
    
    # OCR
    DEFAULT_OCR_ENGINE: str = "paddleocr"
    OCR_LANGUAGES: str = "en,hi,ta,te"  # comma based
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
