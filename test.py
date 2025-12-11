#!/usr/bin/env python3
"""
Test script for Chatterbox TTS integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from text_to_speech import TextToSpeech
import time

def test_chatterbox_tts():
    """Test the upgraded Chatterbox TTS functionality"""
    print("=== Chatterbox TTS Integration Test ===\n")
    
    # Initialize TTS
    print("1. Initializing TTS engine...")
    tts = TextToSpeech()
    
    # Show engine info
    info = tts.get_engine_info()
    print(f"Engine: {info['engine']}")
    print(f"Device: {info['device']}")
    print(f"Multilingual: {info['multilingual']}")
    print(f"Voice Cloning: {info['voice_cloning']}")
    print(f"Emotion Control: {info['emotion_control']}")
    print(f"Available Languages: {info['languages']}\n")
    
    # Test basic English speech
    print("2. Testing basic English speech...")
    tts.speak("Hello! This is a test of the new Chatterbox TTS system.", blocking=True)
    time.sleep(1)
    
    # Test multilingual if available
    if info['multilingual']:
        print("3. Testing multilingual capabilities...")
        
        multilingual_tests = [
            ("Bonjour! Comment allez-vous?", "fr", "French"),
            ("¡Hola! ¿Cómo estás?", "es", "Spanish"),
            ("Guten Tag! Wie geht es Ihnen?", "de", "German"),
            ("你好！你好吗？", "zh", "Chinese"),
            ("こんにちは！元気ですか？", "ja", "Japanese"),
            ("नमस्ते! आप कैसे हैं?", "hi", "Hindi")
        ]
        
        for text, lang, lang_name in multilingual_tests:
            print(f"   Testing {lang_name} ({lang}): {text}")
            tts.speak(text, language=lang, blocking=True)
            time.sleep(1)
    
    # Test emotion control if available
    if info['emotion_control']:
        print("\n4. Testing emotion control...")
        
        emotion_tests = [
            ("This is neutral speech.", 0.5, "Neutral"),
            ("This is more expressive speech!", 1.2, "Expressive"),
            ("This is very dramatic speech!", 1.8, "Very Dramatic")
        ]
        
        for text, exag, desc in emotion_tests:
            print(f"   Testing {desc} (exaggeration={exag}): {text}")
            tts.speak_with_emotion(text, exaggeration=exag)
            time.sleep(2)  # Wait for speech to complete
    
    # Test different speaking speeds
    print("\n5. Testing speaking speed control...")
    speed_tests = [
        ("This is fast speech.", 1.5, "Fast"),
        ("This is normal speech.", 1.0, "Normal"),
        ("This is slow and natural speech.", 0.3, "Slow & Natural")
    ]
    
    for text, cfg, desc in speed_tests:
        print(f"   Testing {desc} (cfg={cfg}): {text}")
        tts.speak_with_emotion(text, cfg=cfg)
        time.sleep(3)
    
    # Test random speech
    print("\n6. Testing random speech generation...")
    phrase = tts.test_speech()
    print(f"Random phrase: {phrase}")
    time.sleep(2)
    
    print("\n=== Test Complete ===")
    print("If you heard speech output, Chatterbox TTS is working correctly!")
    
    # Cleanup
    tts.cleanup()

def test_installation_requirements():
    """Check if all required packages are installed"""
    print("=== Installation Requirements Check ===\n")
    
    requirements = [
        ("torch", "PyTorch for deep learning"),
        ("torchaudio", "Audio processing for PyTorch"),
        ("chatterbox-tts", "Chatterbox TTS models"),
        ("pygame", "Audio playback (recommended)"),
        ("playsound", "Alternative audio playback")
    ]
    
    missing_packages = []
    
    for package, description in requirements:
        try:
            if package == "chatterbox-tts":
                import chatterbox
            else:
                __import__(package)
            print(f"✓ {package}: {description}")
        except ImportError:
            print(f"✗ {package}: {description} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("\nTo install missing packages, run:")
        if "torch" in missing_packages or "torchaudio" in missing_packages:
            print("pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu")
        if "chatterbox-tts" in missing_packages:
            print("pip install chatterbox-tts")
        if "pygame" in missing_packages:
            print("pip install pygame")
        if "playsound" in missing_packages:
            print("pip install playsound")
    else:
        print("\n✓ All packages are installed!")
    
    return len(missing_packages) == 0

if __name__ == "__main__":
    print("Chatterbox TTS Integration Test\n")
    
    # Check installation first
    if test_installation_requirements():
        print("\nProceeding with TTS test...\n")
        test_chatterbox_tts()
    else:
        print("\nPlease install missing packages before running the TTS test.")
        print("You can still test the fallback pyttsx3 functionality.")
        
        response = input("\nWould you like to test with pyttsx3 fallback? (y/n): ")
        if response.lower().startswith('y'):
            test_chatterbox_tts()
