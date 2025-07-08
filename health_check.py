#!/usr/bin/env python3
"""AI Health Copilot - Enhanced Setup Validation"""

import sys
import requests
import json
from pathlib import Path

def validate_setup():
    """Comprehensive setup validation"""
    print("🧑‍⚕️ AI Health Copilot - Enhanced Setup Validation")
    print("=" * 60)
    
    checks_passed = 0
    total_checks = 5
    
    # 1. Check Python packages
    print("\n📦 Checking Python packages...")
    required_packages = ['streamlit', 'requests', 'pandas', 'numpy', 'sklearn', 'plotly']
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Install with: pip install {package}")
            return False
    
    checks_passed += 1
    
    # 2. Check required files
    print("\n📁 Checking required files...")
    required_files = ['app.py', 'requirements.txt', 'diabetes.csv', 'heart.csv', 'parkinsons.csv']
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            return False
    
    checks_passed += 1
    
    # 3. Check datasets
    print("\n📊 Validating datasets...")
    try:
        import pandas as pd
        
        # Check diabetes dataset
        diabetes_df = pd.read_csv('diabetes.csv')
        assert 'Outcome' in diabetes_df.columns
        print(f"✅ diabetes.csv ({len(diabetes_df)} rows)")
        
        # Check heart dataset
        heart_df = pd.read_csv('heart.csv')
        assert 'target' in heart_df.columns
        print(f"✅ heart.csv ({len(heart_df)} rows)")
        
        # Check parkinsons dataset
        parkinsons_df = pd.read_csv('parkinsons.csv')
        assert 'status' in parkinsons_df.columns
        print(f"✅ parkinsons.csv ({len(parkinsons_df)} rows)")
        
    except Exception as e:
        print(f"❌ Dataset validation failed: {e}")
        return False
    
    checks_passed += 1
    
    # 4. Test ML models
    print("\n🤖 Testing ML model training...")
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        # Quick test with diabetes data
        X = diabetes_df.drop('Outcome', axis=1)
        y = diabetes_df['Outcome']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        
        print(f"✅ ML models working (Accuracy: {accuracy:.2f})")
    
    except Exception as e:
        print(f"❌ ML model test failed: {e}")
        return False
    
    checks_passed += 1
    
    # 5. Check API configuration
    print("\n🔑 Testing API configuration...")
    secrets_file = Path('.streamlit/secrets.toml')
    
    if secrets_file.exists():
        try:
            with open(secrets_file, 'r') as f:
                content = f.read()
            
            if 'OPENROUTER_API_KEY' in content:
                api_key = None
                for line in content.split('\n'):
                    if 'OPENROUTER_API_KEY' in line and '=' in line:
                        api_key = line.split('=')[1].strip().strip('"').strip("'")
                        break
                
                if api_key and len(api_key) > 20:
                    print("✅ API key configured")
                    checks_passed += 1
                else:
                    print("⚠️ API key format issue")
            else:
                print("❌ OPENROUTER_API_KEY not found")
        except Exception as e:
            print(f"❌ Error reading secrets: {e}")
    else:
        print("⚠️ secrets.toml not found (will use fallback)")
        checks_passed += 1  # Allow deployment without API key
    
    # Results
    print("\n" + "=" * 60)
    print(f"📊 Validation Results: {checks_passed}/{total_checks} passed")
    
    if checks_passed >= 4:  # Allow missing API key
        print("🎉 AI Health Copilot is ready for deployment!")
        print("\n🚀 Next steps:")
        print("1. Run locally: streamlit run app.py")
        print("2. Push to GitHub repository")
        print("3. Deploy on Streamlit Cloud")
        print("4. Add API key in Streamlit Cloud secrets")
        return True
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = validate_setup()
    sys.exit(0 if success else 1)
