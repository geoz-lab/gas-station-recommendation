#!/usr/bin/env python3
"""
Configure Claude API Key
"""

import os
from pathlib import Path

def update_env_with_claude():
    """Update .env file with Claude API key"""
    claude_key = "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"
    
    # Read existing .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
        
        # Replace the placeholder with actual key
        content = content.replace("your_claude_api_key_here", claude_key)
        
        # Write back to file
        with open(env_file, "w") as f:
            f.write(content)
        
        print(f"✅ Updated {env_file} with Claude API key")
    else:
        print("❌ .env file not found. Please run configure_api.py first.")

def test_claude_api():
    """Test the Claude API"""
    print("\n" + "="*60)
    print("🧪 Testing Claude API")
    print("="*60)
    
    try:
        import requests
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": "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",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 100,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello! Can you help me analyze gas station options? I need to find the best one based on price, distance, and travel time."
                }
            ]
        }
        
        print("🤖 Testing Claude API connection...")
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            print("✅ Claude API is working!")
            print(f"🤖 Response: {content[:100]}...")
        else:
            print(f"❌ Claude API error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Claude API test failed: {e}")

def test_with_real_data():
    """Test Claude API with real gas station data"""
    print("\n" + "="*60)
    print("🧪 Testing Claude with Real Gas Station Data")
    print("="*60)
    
    try:
        import requests
        
        # Sample gas station data
        stations = [
            {
                'name': 'Chevron Station',
                'price_per_gallon': 4.17,
                'distance_miles': 0.7,
                'travel_time_minutes': 1,
                'total_cost': 41.93,
                'travel_cost': 0.23
            },
            {
                'name': 'Shell Station', 
                'price_per_gallon': 4.18,
                'distance_miles': 0.5,
                'travel_time_minutes': 0,
                'total_cost': 41.97,
                'travel_cost': 0.17
            }
        ]
        
        # Format data for Claude
        prompt = "Analyze these gas stations and recommend the best one:\n\n"
        for i, station in enumerate(stations, 1):
            prompt += f"Station {i}: {station['name']}\n"
            prompt += f"- Price: ${station['price_per_gallon']}/gallon\n"
            prompt += f"- Distance: {station['distance_miles']} miles\n"
            prompt += f"- Travel time: {station['travel_time_minutes']} minutes\n"
            prompt += f"- Total cost: ${station['total_cost']}\n\n"
        
        prompt += "Which station would you recommend and why?"
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": "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",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 300,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        print("🤖 Testing Claude with gas station analysis...")
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            print("✅ Claude API analysis working!")
            print(f"🤖 Analysis: {content}")
        else:
            print(f"❌ Claude API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Claude API test failed: {e}")

def main():
    """Main configuration function"""
    print("🚀 Configuring Claude API Key")
    print("="*60)
    
    # Update .env file
    update_env_with_claude()
    
    print("\n✅ Claude API key configured successfully!")
    print("Your API key has been saved to the .env file.")
    
    # Test the API
    test_claude_api()
    test_with_real_data()
    
    print("\n" + "="*60)
    print("🎉 Claude API Setup Complete!")
    print("="*60)
    print("Your app is now configured to use real AI analysis.")
    print("\nNext steps:")
    print("1. Run the test: python test_app.py")
    print("2. Run the app: python main.py")
    print("3. Enjoy real AI-powered gas station recommendations!")

if __name__ == "__main__":
    main() 