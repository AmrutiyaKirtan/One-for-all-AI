#!/usr/bin/env python3
"""
Installation script for Chatterbox TTS integration
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required for Chatterbox TTS")
        return False
    
    print("✓ Python version is compatible")
    return True

def install_chatterbox_tts():
    """Install Chatterbox TTS and dependencies"""
    print("=== Chatterbox TTS Installation ===\n")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install PyTorch (CPU version for compatibility)
    if not run_command(
        "pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu",
        "Installing PyTorch (CPU version)"
    ):
        print("Failed to install PyTorch. Trying alternative...")
        if not run_command("pip install torch torchaudio", "Installing PyTorch (default)"):
            return False
    
    # Install Chatterbox TTS
    if not run_command("pip install chatterbox-tts", "Installing Chatterbox TTS"):
        return False
    
    # Install audio playback libraries
    print("\nInstalling audio playback libraries...")
    pygame_success = run_command("pip install pygame", "Installing pygame")
    playsound_success = run_command("pip install playsound", "Installing playsound")
    
    if not pygame_success and not playsound_success:
        print("⚠️  Warning: No audio playback library installed. Audio will be generated but not played.")
    
    # Install other dependencies
    run_command("pip install numpy", "Installing numpy")
    
    print("\n=== Installation Complete ===")
    print("✓ Chatterbox TTS should now be available!")
    print("\nTo test the installation, run:")
    print("python test.py")
    
    return True

def install_gpu_support():
    """Install GPU support for faster inference"""
    print("\n=== GPU Support Installation ===")
    print("This will install CUDA-enabled PyTorch for faster TTS generation.")
    
    response = input("Do you want to install GPU support? (y/n): ")
    if not response.lower().startswith('y'):
        return
    
    # Check for NVIDIA GPU
    try:
        result = subprocess.run("nvidia-smi", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ NVIDIA GPU detected")
            
            # Install CUDA version of PyTorch
            run_command(
                "pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118",
                "Installing PyTorch with CUDA support"
            )
        else:
            print("✗ No NVIDIA GPU detected. Keeping CPU version.")
    except FileNotFoundError:
        print("✗ nvidia-smi not found. No GPU support available.")

if __name__ == "__main__":
    print("Chatterbox TTS Installation Script")
    print("This will install Chatterbox TTS and all required dependencies.\n")
    
    if install_chatterbox_tts():
        install_gpu_support()
        
        print("\n" + "="*50)
        print("Installation complete! Next steps:")
        print("1. Run 'python test.py' to test the installation")
        print("2. Run 'python main.py' to start your AI assistant")
        print("3. Enjoy high-quality multilingual TTS!")
    else:
        print("\n" + "="*50)
        print("Installation failed. Please check the error messages above.")
        print("You can still use the basic pyttsx3 TTS functionality.")