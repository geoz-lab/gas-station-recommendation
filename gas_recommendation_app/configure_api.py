#!/usr/bin/env python3
"""
Quick API Configuration Script
"""

import os
from pathlib import Path

def configure_google_maps_api():
    """Configure Google Maps API key"""
    api_key = "AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk"
    
    # Create .env file
    env_content = f"""# Gas Station Recommendation App - Environment Variables

# Google Maps API Key (for gas station search and directions)
GOOGLE_MAPS_API_KEY={api_key}

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
    
    env_file = Path(".env")
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"✅ Created {env_file} with your Google Maps API key")
    return env_file

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

def test_google_maps_api():
    """Test the Google Maps API"""
    print("\n" + "="*60)
    print("🧪 Testing Google Maps API")
    print("="*60)
    
    try:
        import requests
        
        # Test Geocoding API
        print("🔍 Testing Geocoding API...")
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': 'San Francisco, CA',
            'key': 'AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk'
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                location = data['results'][0]['geometry']['location']
                print(f"✅ Geocoding API working! San Francisco coordinates: {location}")
            else:
                print(f"❌ Geocoding API error: {data.get('status')}")
        else:
            print(f"❌ Geocoding API HTTP error: {response.status_code}")
        
        # Test Places API
        print("\n🏪 Testing Places API (gas stations)...")
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': '37.7749,-122.4194',  # San Francisco
            'radius': 5000,  # 5km
            'type': 'gas_station',
            'key': 'AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk'
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                stations = data.get('results', [])
                print(f"✅ Places API working! Found {len(stations)} gas stations")
                
                # Show first few stations
                for i, station in enumerate(stations[:3]):
                    name = station.get('name', 'Unknown')
                    vicinity = station.get('vicinity', 'Unknown address')
                    print(f"   {i+1}. {name} - {vicinity}")
            else:
                print(f"❌ Places API error: {data.get('status')}")
        else:
            print(f"❌ Places API HTTP error: {response.status_code}")
        
        # Test Directions API
        print("\n🗺️  Testing Directions API...")
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            'origin': 'San Francisco, CA',
            'destination': 'Oakland, CA',
            'key': 'AIzaSyDjNxcwyJWryuErYs9dD6VPuyqPKmFgjjk'
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                route = data['routes'][0]['legs'][0]
                distance = route['distance']['text']
                duration = route['duration']['text']
                print(f"✅ Directions API working! SF to Oakland: {distance}, {duration}")
            else:
                print(f"❌ Directions API error: {data.get('status')}")
        else:
            print(f"❌ Directions API HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")

def main():
    """Main configuration function"""
    print("🚀 Configuring Google Maps API Key")
    print("="*60)
    
    # Configure API key
    configure_google_maps_api()
    update_config_for_env()
    
    print("\n✅ Google Maps API key configured successfully!")
    print("Your API key has been saved to the .env file.")
    
    # Test the API
    test_google_maps_api()
    
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("Your app is now configured to use real Google Maps data.")
    print("\nNext steps:")
    print("1. Run the test: python test_app.py")
    print("2. Run the app: python main.py")
    print("3. Optionally add Claude/OpenAI API keys for real AI analysis")

if __name__ == "__main__":
    main() 