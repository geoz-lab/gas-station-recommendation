#!/usr/bin/env python3
"""
Setup script for Gas Station Recommendation App
"""

from secure_config import setup_api_keys

def main():
    """Main setup function"""
    print("🚀 Gas Station Recommendation App Setup")
    print("=" * 50)
    print("This script will help you configure your API keys securely.")
    print("Your API keys will be encrypted and stored safely on your computer.\n")
    
    try:
        setup_api_keys()
        print("\n🎉 Setup complete!")
        print("You can now run the app with: python web_app.py")
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")

if __name__ == "__main__":
    main() 