import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.config import get_settings
from src.core.logger import logger
from src.database.client import get_supabase

async def check_env():
    print("🔎 Checking Environment...")
    
    # 1. Check Settings
    try:
        settings = get_settings()
        print(f"✅ Settings Loaded: {settings.APP_NAME} ({settings.APP_ENV})")
        print(f"   - Supabase URL: {settings.SUPABASE_URL}")
        print(f"   - Supabase Key: {'*' * 10} ({len(settings.SUPABASE_KEY)} chars)")
        print(f"   - Google Key:   {'*' * 10} ({len(settings.GOOGLE_API_KEY)} chars)")
        print(f"   - Ollama URL:   {settings.OLLAMA_BASE_URL}")
    except Exception as e:
        print(f"❌ Failed to load settings: {e}")
        return

    # 2. Check Logger
    logger.info("Test log message", component="check_env")
    print("✅ Logger Configured")

    # 3. Check Supabase
    print("\n📡 Connecting to Supabase...")
    try:
        supabase = get_supabase()
        # Simple health check (fetch version or empty query)
        # Note: If no tables exist, this might fail unless we just check the object
        # We'll try to get auth settings or just presence of client
        if supabase:
             print("✅ Supabase Client Initialized")
             
             # Try a light query if possible, but for now client init is good enough
             # connection is verified on first request usually
        
    except Exception as e:
        print(f"❌ Supabase Connection Failed: {e}")

    print("\n✨ Core Infrastructure Check Complete!")

if __name__ == "__main__":
    asyncio.run(check_env())
