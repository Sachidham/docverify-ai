from supabase import create_client, Client
from src.core.config import get_settings
from src.core.logger import logger

settings = get_settings()

class SupabaseManager:
    """
    Singleton manager for Supabase client.
    """
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            logger.info("Initializing Supabase client...", url=settings.SUPABASE_URL)
            try:
                cls._instance = create_client(
                    settings.SUPABASE_URL, 
                    settings.SUPABASE_KEY
                )
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error("Failed to initialize Supabase client", error=str(e))
                raise e
        return cls._instance

def get_supabase() -> Client:
    """Helper to get client instance."""
    return SupabaseManager.get_client()
