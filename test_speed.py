#!/usr/bin/env python3
"""
Test TTS speed optimizations
"""

import time
import os
from text_to_speech import TextToSpeech

def test_tts_speed():
    """Test TTS generation speed"""
    print("=== TTS Speed Test ===\n")
    
    # Load environment variables
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass
    
    tts = TextToSpeech()
    
    # Test short response (should use fast mode)
    print("Testing short response (fast mode):")
    short_text = "Hello there!"
    start_time = time.time()
    tts.speak(short_text, blocking=True, fast_mode=True)
    fast_time = time.time() - start_time
    print(f"Fast mode time: {fast_time:.2f} seconds\n")
    
    # Test normal response
    print("Testing normal response:")
    normal_text = "This is a longer response that should use normal generation settings for better quality."
    start_time = time.time()
    tts.speak(normal_text, blocking=True, fast_mode=False)
    normal_time = time.time() - start_time
    print(f"Normal mode time: {normal_time:.2f} seconds\n")
    
    print(f"Speed improvement: {((normal_time - fast_time) / normal_time * 100):.1f}% faster")

if __name__ == "__main__":
    test_tts_speed()