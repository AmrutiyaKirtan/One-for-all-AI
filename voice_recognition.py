"""
Voice Recognition Module
Handles speech-to-text functionality using the SpeechRecognition library
"""

import speech_recognition as sr
import threading
import time
import sys
import platform

class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.callbacks = {}
        
        # Configure recognizer
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Try to initialize microphone
        self.init_microphone()
    
    def init_microphone(self):
        """Initialize microphone with fallback options"""
        try:
            # Try to use default microphone
            self.microphone = sr.Microphone()
            self.calibrate_microphone()
            print("✓ Microphone initialized successfully")
        except Exception as e:
            print(f"Failed to initialize microphone: {e}")
            if "Could not find PyAudio" in str(e):
                print("💡 To enable voice recognition:")
                print("   1. Run: python install_pyaudio.py")
                print("   2. Or continue with text input only")
            print("Microphone functionality will be limited")
            self.microphone = None
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        if not self.microphone:
            return
        try:
            with self.microphone as source:
                print("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone calibrated")
        except Exception as e:
            print(f"Microphone calibration failed: {e}")
            self.microphone = None
    
    def set_callbacks(self, on_result=None, on_error=None, on_start=None, on_stop=None):
        """Set callback functions for voice recognition events"""
        self.callbacks = {
            'on_result': on_result,
            'on_error': on_error,
            'on_start': on_start,
            'on_stop': on_stop
        }
    
    def start_listening(self):
        """Start continuous voice recognition"""
        if self.is_listening:
            return
        
        if not self.microphone:
            if self.callbacks.get('on_error'):
                self.callbacks['on_error']("Microphone not available. Please install PyAudio or use text input.")
            return
        
        self.is_listening = True
        
        if self.callbacks.get('on_start'):
            self.callbacks['on_start']()
        
        try:
            while self.is_listening:
                try:
                    # Listen for audio with timeout
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    
                    if text and self.callbacks.get('on_result'):
                        self.callbacks['on_result'](text)
                        
                except sr.WaitTimeoutError:
                    # Timeout is normal, continue listening
                    pass
                except sr.UnknownValueError:
                    # Could not understand audio, continue listening
                    pass
                except sr.RequestError as e:
                    if self.callbacks.get('on_error'):
                        self.callbacks['on_error'](f"Recognition service error: {e}")
                    break
                except Exception as e:
                    if self.callbacks.get('on_error'):
                        self.callbacks['on_error'](f"Unexpected error: {e}")
                    break
                    
        finally:
            self.is_listening = False
            if self.callbacks.get('on_stop'):
                self.callbacks['on_stop']()
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
    
    def recognize_once(self, timeout=5):
        """Recognize speech once with timeout"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Recognition service error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_listening()
    
    def test_microphone(self):
        """Test if microphone is working"""
        try:
            with self.microphone as source:
                print("Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=3)
            
            text = self.recognizer.recognize_google(audio)
            print(f"Microphone test successful. Heard: {text}")
            return True
            
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False