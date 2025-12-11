#!/usr/bin/env python3
"""
PyAudio Installation Script
Tries multiple methods to install PyAudio on Windows
"""

import subprocess
import sys
import platform
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} successful!")
            return True
        else:
            print(f"✗ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {description} failed: {e}")
        return False

def check_pyaudio():
    """Check if PyAudio is already installed"""
    try:
        import pyaudio
        print("✓ PyAudio is already installed!")
        return True
    except ImportError:
        print("✗ PyAudio not found, attempting installation...")
        return False

def install_pyaudio_windows():
    """Install PyAudio on Windows using multiple methods"""
    print("=== PyAudio Installation for Windows ===\n")
    
    # Check if already installed
    if check_pyaudio():
        return True
    
    # Method 1: Direct pip install
    if run_command("pip install pyaudio", "Method 1: Direct pip install"):
        return check_pyaudio()
    
    # Method 2: Using pipwin
    print("\nTrying Method 2: Using pipwin...")
    if run_command("pip install pipwin", "Installing pipwin"):
        if run_command("pipwin install pyaudio", "Installing PyAudio via pipwin"):
            return check_pyaudio()
    
    # Method 3: Precompiled wheel for Python 3.11
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if python_version == "3.11":
        wheel_url = "https://download.lfd.uci.edu/pythonlibs/archived/pyaudio-0.2.11-cp311-cp311-win_amd64.whl"
        if run_command(f"pip install {wheel_url}", "Method 3: Installing precompiled wheel"):
            return check_pyaudio()
    
    # Method 4: Try conda if available
    if run_command("conda install -c anaconda pyaudio", "Method 4: Conda install"):
        return check_pyaudio()
    
    print("\n❌ All PyAudio installation methods failed.")
    print("\nAlternative solutions:")
    print("1. Install Visual Studio Build Tools:")
    print("   https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    print("2. Use Windows Speech Recognition (no PyAudio needed)")
    print("3. Continue with text input only")
    
    return False

def install_pyaudio_mac():
    """Install PyAudio on macOS"""
    print("=== PyAudio Installation for macOS ===\n")
    
    if check_pyaudio():
        return True
    
    # Install portaudio first
    if run_command("brew install portaudio", "Installing portaudio via Homebrew"):
        if run_command("pip install pyaudio", "Installing PyAudio"):
            return check_pyaudio()
    
    return False

def install_pyaudio_linux():
    """Install PyAudio on Linux"""
    print("=== PyAudio Installation for Linux ===\n")
    
    if check_pyaudio():
        return True
    
    # Try apt-get first (Ubuntu/Debian)
    if run_command("sudo apt-get install python3-pyaudio", "Installing via apt-get"):
        return check_pyaudio()
    
    # Try installing development packages and pip
    if run_command("sudo apt-get install portaudio19-dev python3-all-dev", "Installing development packages"):
        if run_command("pip install pyaudio", "Installing PyAudio via pip"):
            return check_pyaudio()
    
    return False

def main():
    """Main installation function"""
    system = platform.system()
    
    print(f"Detected OS: {system}")
    print(f"Python version: {sys.version}")
    
    if system == "Windows":
        success = install_pyaudio_windows()
    elif system == "Darwin":
        success = install_pyaudio_mac()
    elif system == "Linux":
        success = install_pyaudio_linux()
    else:
        print(f"Unsupported OS: {system}")
        success = False
    
    if success:
        print("\n🎉 PyAudio installation successful!")
        print("You can now use voice recognition in your AI assistant.")
        
        # Test microphone
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            print(f"Available audio devices: {p.get_device_count()}")
            p.terminate()
        except Exception as e:
            print(f"PyAudio installed but microphone test failed: {e}")
    else:
        print("\n⚠️  PyAudio installation failed.")
        print("Your AI assistant will work with text input only.")
        print("Voice recognition will be disabled.")

if __name__ == "__main__":
    main()