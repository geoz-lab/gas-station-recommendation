"""
Configuration settings for Gas Station Recommendation App
"""

import os
from typing import Optional
from pathlib import Path

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

# Load .env file if it exists
load_env_file()

class Config:
    """Application configuration"""
    
    # API Keys (set these as environment variables)
    GOOGLE_MAPS_API_KEY: Optional[str] = os.getenv('GOOGLE_MAPS_API_KEY')
    CLAUDE_API_KEY: Optional[str] = os.getenv('CLAUDE_API_KEY')
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')  # Alternative LLM
    
    # Default settings
    DEFAULT_MPG: float = float(os.getenv('DEFAULT_MPG', '25.0'))
    DEFAULT_TANK_SIZE: float = float(os.getenv('DEFAULT_TANK_SIZE', '15.0'))
    
    # Search parameters
    DEFAULT_SEARCH_RADIUS_MILES: float = float(os.getenv('DEFAULT_SEARCH_RADIUS_MILES', '10.0'))
    MAX_TRAVEL_TIME_MINUTES: int = int(os.getenv('MAX_TRAVEL_TIME_MINUTES', '20'))
    TYPICAL_SPEED_HIGHWAY: int = 60  # mph
    TYPICAL_SPEED_LOCAL: int = 40    # mph
    
    # LLM settings
    LLM_MODEL: str = "claude-3-5-haiku-20241022"  # or "gpt-4"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.1
    
    # Map service settings
    MAP_PROVIDER: str = "google"  # or "openstreetmap" for fallback
    
    # Default location (San Francisco)
    DEFAULT_LATITUDE: float = 37.7749
    DEFAULT_LONGITUDE: float = -122.4194
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required API keys are set"""
        if not cls.GOOGLE_MAPS_API_KEY:
            print("⚠️  Warning: GOOGLE_MAPS_API_KEY not set. Some features may not work.")
            return False
        return True
    
    @classmethod
    def get_llm_api_key(cls) -> Optional[str]:
        """Get the appropriate LLM API key"""
        if cls.CLAUDE_API_KEY:
            return cls.CLAUDE_API_KEY
        elif cls.OPENAI_API_KEY:
            return cls.OPENAI_API_KEY
        else:
            print("⚠️  Warning: No LLM API key found. Using mock responses.")
            return None
