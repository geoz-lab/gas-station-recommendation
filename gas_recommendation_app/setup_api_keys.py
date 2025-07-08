#!/usr/bin/env python3
"""
API Key Setup Script for Gas Station Recommendation App
"""

import os
import sys
from pathlib import Path

def setup_google_maps_api():
    """Guide user through Google Maps API setup"""
    print("\n" + "="*60)
    print("🗺️  Google Maps API Setup")
    print("="*60)
    
    print("""
To get a Google Maps API key:

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select existing one
3. Enable these APIs:
   - Places API
   - Directions API
   - Geocoding API
4. Go to Credentials → Create Credentials → API Key
5. Copy your API key

Note: Google Maps API has usage limits and costs. 
For development, you get $200 free credit monthly.
""")
    
    api_key = input("Enter your Google Maps API key (or press Enter to skip): ").strip()
    
    if api_key:
        return api_key
    else:
        print("⚠️  Google Maps API key not provided. Will use mock data.")
        return None

def setup_claude_api():
    """Guide user through Claude API setup"""
    print("\n" + "="*60)
    print("🤖 Claude API Setup")
    print("="*60)
    
    print("""
To get a Claude API key:

1. Go to Anthropic Console: https://console.anthropic.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy your API key

Note: Claude API has usage limits. 
You get free credits when you sign up.
""")
    
    api_key = input("Enter your Claude API key (or press Enter to skip): ").strip()
    
    if api_key:
        return api_key
    else:
        print("⚠️  Claude API key not provided. Will use mock analysis.")
        return None

def setup_openai_api():
    """Guide user through OpenAI API setup"""
    print("\n" + "="*60)
    print("🤖 OpenAI API Setup (Alternative)")
    print("="*60)
    
    print("""
To get an OpenAI API key:

1. Go to OpenAI Platform: https://platform.openai.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy your API key

Note: OpenAI API has usage costs.
You get free credits when you sign up.
""")
    
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if api_key:
        return api_key
    else:
        print("⚠️  OpenAI API key not provided.")
        return None

def create_env_file(google_key=None, claude_key=None, openai_key=None):
    """Create .env file with API keys"""
    env_content = """# Gas Station Recommendation App - Environment Variables
# Copy this file to .env and fill in your API keys

# Google Maps API Key (for gas station search and directions)
GOOGLE_MAPS_API_KEY={google_key}

# Claude API Key (for AI analysis - preferred)
CLAUDE_API_KEY={claude_key}

# OpenAI API Key (alternative LLM)
OPENAI_API_KEY={openai_key}

# Optional: Customize default settings
# DEFAULT_MPG=25.0
# DEFAULT_TANK_SIZE=15.0
# DEFAULT_SEARCH_RADIUS_MILES=10.0
# MAX_TRAVEL_TIME_MINUTES=20
""".format(
        google_key=google_key or "your_google_maps_api_key_here",
        claude_key=claude_key or "your_claude_api_key_here", 
        openai_key=openai_key or "your_openai_api_key_here"
    )
    
    env_file = Path(".env")
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"\n✅ Created {env_file}")
    return env_file

def create_env_example():
    """Create .env.example file"""
    example_content = """# Gas Station Recommendation App - Environment Variables Example
# Copy this file to .env and fill in your actual API keys

# Google Maps API Key (for gas station search and directions)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Claude API Key (for AI analysis - preferred)
CLAUDE_API_KEY=your_claude_api_key_here

# OpenAI API Key (alternative LLM)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Customize default settings
# DEFAULT_MPG=25.0
# DEFAULT_TANK_SIZE=15.0
# DEFAULT_SEARCH_RADIUS_MILES=10.0
# MAX_TRAVEL_TIME_MINUTES=20
"""
    
    example_file = Path(".env.example")
    with open(example_file, "w") as f:
        f.write(example_content)
    
    print(f"✅ Created {example_file}")
    return example_file

def update_config_for_env():
    """Update config.py to load from .env file"""
    config_content = '''"""
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
    LLM_MODEL: str = "claude-3-sonnet-20240229"  # or "gpt-4"
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
'''
    
    config_file = Path("config.py")
    with open(config_file, "w") as f:
        f.write(config_content)
    
    print(f"✅ Updated {config_file} to load from .env file")

def test_api_keys():
    """Test the configured API keys"""
    print("\n" + "="*60)
    print("🧪 Testing API Keys")
    print("="*60)
    
    # Import after potential config update
    from config import Config
    
    print(f"Google Maps API Key: {'✅ Set' if Config.GOOGLE_MAPS_API_KEY else '❌ Not set'}")
    print(f"Claude API Key: {'✅ Set' if Config.CLAUDE_API_KEY else '❌ Not set'}")
    print(f"OpenAI API Key: {'✅ Set' if Config.OPENAI_API_KEY else '❌ Not set'}")
    
    if Config.GOOGLE_MAPS_API_KEY:
        print("\n🔍 Testing Google Maps API...")
        try:
            import requests
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': 'San Francisco',
                'key': Config.GOOGLE_MAPS_API_KEY
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    print("✅ Google Maps API is working!")
                else:
                    print(f"❌ Google Maps API error: {data.get('status')}")
            else:
                print(f"❌ Google Maps API HTTP error: {response.status_code}")
        except Exception as e:
            print(f"❌ Google Maps API test failed: {e}")
    
    if Config.CLAUDE_API_KEY:
        print("\n🤖 Testing Claude API...")
        try:
            import requests
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": Config.CLAUDE_API_KEY,
                "anthropic-version": "2023-06-01"
            }
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}]
            }
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                print("✅ Claude API is working!")
            else:
                print(f"❌ Claude API error: {response.status_code}")
        except Exception as e:
            print(f"❌ Claude API test failed: {e}")

def main():
    """Main setup function"""
    print("🚀 Gas Station Recommendation App - API Setup")
    print("="*60)
    
    print("This script will help you set up API keys for real data.")
    print("You can skip any API key if you want to use mock data.")
    
    # Get API keys
    google_key = setup_google_maps_api()
    claude_key = setup_claude_api()
    openai_key = setup_openai_api()
    
    # Create files
    env_file = create_env_file(google_key, claude_key, openai_key)
    create_env_example()
    update_config_for_env()
    
    print("\n" + "="*60)
    print("📝 Next Steps:")
    print("="*60)
    print("1. Edit the .env file with your actual API keys")
    print("2. Run the test script: python test_app.py")
    print("3. Run the main app: python main.py")
    print("\nNote: Keep your API keys secure and never commit them to version control!")
    
    # Test the keys
    test_api_keys()
    
    print("\n🎉 Setup complete! Your app is ready to use with real data.")

if __name__ == "__main__":
    main() 