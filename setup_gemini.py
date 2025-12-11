#!/usr/bin/env python3
"""
Setup script for Google Gemini API integration
"""

import os
import sys

def setup_gemini_api():
    """Setup Gemini API key"""
    print("=== Google Gemini API Setup ===\n")
    
    # Check if already configured
    existing_key = os.getenv('GEMINI_API_KEY')
    if existing_key:
        print(f"✓ API key already configured: {existing_key[:10]}...")
        return True
    
    print("To get your free Gemini API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the key (starts with 'AIza...')")
    print()
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    if not api_key.startswith('AIza'):
        print("⚠️  Warning: API key doesn't look like a Gemini key (should start with 'AIza')")
    
    # Set environment variable for current session
    os.environ['GEMINI_API_KEY'] = api_key
    
    # Create a .env file for persistence
    try:
        with open('.env', 'w') as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        print("✓ API key saved to .env file")
    except Exception as e:
        print(f"⚠️  Could not save to .env file: {e}")
    
    # Test the API key
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with a simple prompt
        response = model.generate_content("Say 'Hello, I am Gemini AI!' in a friendly way.")
        print(f"\n✓ API key test successful!")
        print(f"Gemini response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

def load_env_file():
    """Load environment variables from .env file"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✓ Environment variables loaded from .env")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"⚠️  Error loading .env file: {e}")

if __name__ == "__main__":
    print("Google Gemini API Setup for AI Assistant\n")
    
    # Load existing .env file
    load_env_file()
    
    if setup_gemini_api():
        print("\n🎉 Gemini API setup complete!")
        print("Your AI assistant now has intelligent conversation capabilities!")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Try asking complex questions like:")
        print("   - 'Explain quantum computing'")
        print("   - 'Help me plan my day'")
        print("   - 'What's the best way to learn Python?'")
    else:
        print("\n❌ Setup failed. Your assistant will use basic responses only.")
        print("You can run this script again anytime to set up Gemini.")