#!/usr/bin/env python3
"""Health Check Script - Enhanced API Testing"""

import os
import sys
import requests
import json
from pathlib import Path

def test_api_with_key(api_key):
    """Test specific API key"""
    print(f"🔑 Testing API key: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-health-copilot.streamlit.app",
        "X-Title": "AI Health Copilot"
    }
    
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ API key valid and working!")
            return True
        elif response.status_code == 401:
            print("❌ Invalid API key")
            print("💡 Get new key from: https://openrouter.ai/")
            return False
        elif response.status_code == 402:
            print("⚠️ API quota exceeded (but key is valid)")
            return True
        elif response.status_code == 429:
            print("⚠️ Rate limited (but key is valid)")
            return True
        else:
            print(f"⚠️ API returned: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    """Enhanced health check"""
    print("🏥 AI Health Copilot - Enhanced Setup Validation")
    print("=" * 60)
    
    # Check files
    print("\n📁 Checking files:")
    files = ["app.py", "requirements.txt", ".streamlit/secrets.toml"]
    for file in files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
    
    # Test API
    print("\n🔑 Testing API configuration:")
    secrets_file = Path(".streamlit/secrets.toml")
    
    if secrets_file.exists():
        try:
            with open(secrets_file, 'r') as f:
                content = f.read()
            
            # Extract API key
            api_key = None
            for line in content.split('\n'):
                if 'OPENROUTER_API_KEY' in line and '=' in line:
                    api_key = line.split('=')[1].strip().strip('"').strip("'")
                    break
            
            if api_key and len(api_key) > 20:
                if test_api_with_key(api_key):
                    print("🎉 Setup complete! Ready to deploy.")
                    return True
                else:
                    print("❌ API key issue detected")
                    return False
            else:
                print("❌ No valid API key found")
                return False
                
        except Exception as e:
            print(f"❌ Error reading secrets: {e}")
            return False
    else:
        print("❌ secrets.toml not found")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
