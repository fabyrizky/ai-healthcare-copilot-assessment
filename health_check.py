#!/usr/bin/env python3
"""
Health Check Script for AI Health Copilot
Run this script to validate your setup before deployment
"""

import os
import sys
import requests
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version compatible")
    return True

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "app.py",
        "requirements.txt",
        ".streamlit/config.toml",
        ".streamlit/secrets.example.toml",
        "README.md",
        ".gitignore"
    ]
    
    print("\n📁 Checking required files:")
    all_present = True
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_present = False
    
    return all_present

def check_dependencies():
    """Check if required packages can be imported"""
    required_packages = [
        "streamlit",
        "streamlit_option_menu", 
        "requests",
        "numpy",
        "pandas",
        "sklearn"
    ]
    
    print("\n📦 Checking dependencies:")
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "streamlit_option_menu":
                importlib.import_module("streamlit_option_menu")
            elif package == "sklearn":
                importlib.import_module("sklearn")
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_secrets():
    """Check if secrets file exists and has API key"""
    secrets_path = Path(".streamlit/secrets.toml")
    
    print("\n🔐 Checking secrets configuration:")
    
    if not secrets_path.exists():
        print("❌ secrets.toml not found")
        print("💡 Copy secrets.example.toml to secrets.toml and add your API key")
        return False
    
    try:
        with open(secrets_path, 'r') as f:
            content = f.read()
            
        if "your-actual-api-key-here" in content:
            print("⚠️  secrets.toml contains example API key")
            print("💡 Replace with your actual OpenRouter API key")
            return False
        
        if "OPENROUTER_API_KEY" not in content:
            print("❌ OPENROUTER_API_KEY not found in secrets.toml")
            return False
        
        print("✅ secrets.toml configured")
        return True
        
    except Exception as e:
        print(f"❌ Error reading secrets.toml: {e}")
        return False

def check_api_connection():
    """Test OpenRouter API connection"""
    print("\n🌐 Testing API connection:")
    
    try:
        # Try to read API key from secrets
        secrets_path = Path(".streamlit/secrets.toml")
        if not secrets_path.exists():
            print("❌ Cannot test API - secrets.toml not found")
            return False
        
        # Simple connection test
        response = requests.get(
            "https://openrouter.ai/api/v1/models", 
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ OpenRouter API reachable")
            return True
        else:
            print(f"⚠️  OpenRouter API returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection failed: {e}")
        return False

def check_streamlit_config():
    """Validate Streamlit configuration"""
    print("\n⚙️  Checking Streamlit configuration:")
    
    config_path = Path(".streamlit/config.toml")
    if config_path.exists():
        print("✅ config.toml found")
        return True
    else:
        print("⚠️  config.toml not found (optional)")
        return True

def create_test_models():
    """Create dummy models directory"""
    print("\n🤖 Checking model setup:")
    
    models_dir = Path("saved_models")
    if not models_dir.exists():
        try:
            models_dir.mkdir(exist_ok=True)
            print("✅ Created saved_models directory")
            return True
        except Exception as e:
            print(f"❌ Failed to create models directory: {e}")
            return False
    else:
        print("✅ saved_models directory exists")
        return True

def main():
    """Run all health checks"""
    print("🏥 AI Health Copilot - Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Dependencies", check_dependencies),
        ("Secrets Configuration", check_secrets),
        ("API Connection", check_api_connection),
        ("Streamlit Config", check_streamlit_config),
        ("Model Setup", create_test_models)
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
    print(f"📊 Health Check Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All checks passed! Ready for deployment.")
        print("\n🚀 Next steps:")
        print("1. Commit your code to GitHub")
        print("2. Deploy on Streamlit Cloud")
        print("3. Add your API key in deployment secrets")
        return True
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Copy secrets.example.toml to secrets.toml")
        print("- Add your OpenRouter API key to secrets.toml")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
