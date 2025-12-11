#!/usr/bin/env python3
"""
Setup script for Hugging Face authentication
Required for accessing Chatterbox TTS models
"""

import os
import subprocess
import sys

def setup_huggingface_auth():
    """Setup Hugging Face authentication for Chatterbox TTS"""
    print("=== Hugging Face Authentication Setup ===\n")
    
    print("Chatterbox TTS requires authentication with Hugging Face.")
    print("You need to:")
    print("1. Create a Hugging Face account at https://huggingface.co/join")
    print("2. Accept the license for Chatterbox TTS at https://huggingface.co/ResembleAI/chatterbox")
    print("3. Create an access token at https://huggingface.co/settings/tokens")
    print("4. Install huggingface-hub CLI: pip install huggingface-hub")
    print("5. Login with: huggingface-cli login\n")
    
    # Check if huggingface-hub is installed
    try:
        import huggingface_hub
        print("✓ huggingface-hub is installed")
    except ImportError:
        print("Installing huggingface-hub...")
        subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub"], check=True)
        print("✓ huggingface-hub installed")
    
    # Check if user is already logged in
    try:
        from huggingface_hub import whoami
        user_info = whoami()
        print(f"✓ Already logged in as: {user_info['name']}")
        return True
    except Exception:
        print("✗ Not logged in to Hugging Face")
    
    # Prompt for login
    print("\nTo login to Hugging Face:")
    print("1. Run: huggingface-cli login")
    print("2. Enter your access token when prompted")
    print("3. Accept the Chatterbox license at: https://huggingface.co/ResembleAI/chatterbox")
    
    response = input("\nWould you like to login now? (y/n): ")
    if response.lower().startswith('y'):
        try:
            subprocess.run(["huggingface-cli", "login"], check=True)
            print("✓ Login successful!")
            return True
        except subprocess.CalledProcessError:
            print("✗ Login failed. Please try manually.")
            return False
        except FileNotFoundError:
            print("✗ huggingface-cli not found. Please install huggingface-hub.")
            return False
    
    return False

def test_chatterbox_access():
    """Test if we can access Chatterbox TTS models"""
    print("\n=== Testing Chatterbox Access ===")
    
    try:
        from huggingface_hub import hf_hub_download
        
        # Try to access a small file from the Chatterbox repo
        print("Testing access to Chatterbox TTS repository...")
        file_path = hf_hub_download(
            repo_id="ResembleAI/chatterbox",
            filename="README.md",
            cache_dir="./.cache"
        )
        print("✓ Successfully accessed Chatterbox TTS repository!")
        print(f"Downloaded: {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Cannot access Chatterbox TTS: {e}")
        print("\nPlease ensure you have:")
        print("1. Accepted the license at https://huggingface.co/ResembleAI/chatterbox")
        print("2. Logged in with a valid access token")
        return False

if __name__ == "__main__":
    print("Chatterbox TTS Authentication Setup\n")
    
    if setup_huggingface_auth():
        if test_chatterbox_access():
            print("\n✅ Setup complete! You can now use Chatterbox TTS.")
            print("Run 'python test.py' to test the installation.")
        else:
            print("\n❌ Setup incomplete. Please check the requirements above.")
    else:
        print("\n⚠️  Authentication not completed.")
        print("You can still use the pyttsx3 fallback TTS.")
        print("To setup Chatterbox later, run this script again.")