#!/usr/bin/env python3
"""
Health Check Script for AI Health Copilot
Run: python health_check.py
"""

import os
import sys
import requests
import importlib.util
from pathlib import Path

def check_python_version():
    """Check Python compatibility"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version compatible")
    return True

def check_required_files():
    """Check required files exist"""
    files = ["app.py", "requirements.txt", ".streamlit/secrets.toml", "health_check.py"]
    
    print("\n📁 Checking files:")
    all_present = True
    
    for file_path in files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_present = False
    
    return all_present

def check_dependencies():
    """Check package imports"""
    packages = ["streamlit", "requests"]
    
    print("\n📦 Checking dependencies:")
    missing = []
    
    for package in packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n💡 Install with: pip install {' '.join(missing)}")
        return False
    
    return True

def check_api_connection():
    """Test OpenRouter API"""
    print("\n🌐 Testing API connection:")
    
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        
        if response.status_code == 200:
            print("✅ OpenRouter API reachable")
            return True
        else:
            print(f"⚠️ API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_api_key():
    """Test API key validity"""
    print("\n🔑 Testing API key:")
    
    secrets_path = Path(".streamlit/secrets.toml")
    if not secrets_path.exists():
        print("❌ secrets.toml not found")
        return False
    
    try:
        # Read API key from secrets
        with open(secrets_path, 'r') as f:
            content = f.read()
        
        if "your-actual-api-key-here" in content:
            print("⚠️ Using example API key")
            return False
        
        # Extract API key
        for line in content.split('\n'):
            if 'OPENROUTER_API_KEY' in line and '=' in line:
                api_key = line.split('=')[1].strip().strip('"').strip("'")
                break
        else:
            print("❌ API key not found in secrets.toml")
            return False
        
        # Test API call
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [{"role": "user", "content": "Test"}],
            "max_tokens": 10
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ API key valid and working")
            return True
        elif response.status_code == 401:
            print("❌ Invalid API key")
            return False
        elif response.status_code == 402:
            print("⚠️ API quota exceeded")
            return True  # Key is valid, just no credits
        else:
            print(f"⚠️ API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all health checks"""
    print("🏥 AI Health Copilot - Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Dependencies", check_dependencies),
        ("API Connection", check_api_connection),
        ("API Key Test", test_api_key)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All checks passed! Ready for deployment.")
        print("\n🚀 Next steps:")
        print("1. Run: streamlit run app.py")
        print("2. Test all features locally")
        print("3. Deploy to Streamlit Cloud")
    else:
        print("⚠️ Some checks failed. Fix issues above.")
        print("\n💡 Quick fixes:")
        print("- pip install -r requirements.txt")
        print("- Add valid API key to .streamlit/secrets.toml")
        print("- Get free API key from: https://openrouter.ai/")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
