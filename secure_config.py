"""
Secure Configuration for Gas Station Recommendation App
This file handles secure API key management
"""

import os
import json
import base64
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
import getpass

class SecureConfig:
    """Secure configuration management"""
    
    def __init__(self):
        self.config_file = Path(".secure_config")
        self.key_file = Path(".key")
        self.fernet = None
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize encryption key"""
        if not self.key_file.exists():
            # Generate a new key
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Set restrictive permissions
            os.chmod(self.key_file, 0o600)
        
        # Load the key
        with open(self.key_file, 'rb') as f:
            key = f.read()
        self.fernet = Fernet(key)
    
    def save_api_keys(self, api_keys: Dict[str, str]):
        """Save API keys securely"""
        if self.fernet is None:
            raise RuntimeError("Encryption not initialized")
        encrypted_data = self.fernet.encrypt(json.dumps(api_keys).encode())
        with open(self.config_file, 'wb') as f:
            f.write(encrypted_data)
        # Set restrictive permissions
        os.chmod(self.config_file, 0o600)
    
    def load_api_keys(self) -> Dict[str, str]:
        """Load API keys securely"""
        if not self.config_file.exists():
            return {}
        
        try:
            if self.fernet is None:
                raise RuntimeError("Encryption not initialized")
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"⚠️  Error loading secure config: {e}")
            return {}
    
    def setup_api_keys(self):
        """Interactive setup for API keys"""
        print("🔐 Secure API Key Setup")
        print("=" * 50)
        print("This will securely store your API keys in an encrypted file.")
        print("The keys will be encrypted and only accessible by this application.\n")
        
        api_keys = {}
        
        # Google Maps API Key
        print("🗺️  Google Maps API Key")
        print("Get your key from: https://console.cloud.google.com/apis/credentials")
        google_key = getpass.getpass("Enter your Google Maps API key (or press Enter to skip): ")
        if google_key.strip():
            api_keys['GOOGLE_MAPS_API_KEY'] = google_key.strip()
        
        # Claude API Key
        print("\n🤖 Claude AI API Key")
        print("Get your key from: https://console.anthropic.com/")
        claude_key = getpass.getpass("Enter your Claude API key (or press Enter to skip): ")
        if claude_key.strip():
            api_keys['CLAUDE_API_KEY'] = claude_key.strip()
        
        # OpenAI API Key (optional)
        print("\n🤖 OpenAI API Key (optional)")
        print("Get your key from: https://platform.openai.com/api-keys")
        openai_key = getpass.getpass("Enter your OpenAI API key (or press Enter to skip): ")
        if openai_key.strip():
            api_keys['OPENAI_API_KEY'] = openai_key.strip()
        
        if api_keys:
            self.save_api_keys(api_keys)
            print(f"\n✅ Successfully saved {len(api_keys)} API key(s) securely!")
            print("🔒 Your API keys are now encrypted and stored safely.")
        else:
            print("\n⚠️  No API keys were provided. Some features may not work.")
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """Get a specific API key"""
        api_keys = self.load_api_keys()
        return api_keys.get(key_name)

# Global secure config instance
secure_config = SecureConfig()

def setup_api_keys():
    """Convenience function to setup API keys"""
    secure_config.setup_api_keys()

def get_api_key(key_name: str) -> Optional[str]:
    """Convenience function to get API key"""
    return secure_config.get_api_key(key_name) 