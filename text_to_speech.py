"""
Text-to-Speech Module
Handles speech synthesis using Chatterbox TTS (with pyttsx3 fallback)
"""

import threading
import tempfile
import os
import sys
from pathlib import Path

# Try to import Chatterbox TTS
try:
    import torch
    import torchaudio as ta
    from chatterbox.tts import ChatterboxTTS
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    CHATTERBOX_AVAILABLE = True
    print("Chatterbox TTS loaded successfully!")
except ImportError as e:
    print(f"Chatterbox TTS not available: {e}")
    print("Falling back to pyttsx3...")
    CHATTERBOX_AVAILABLE = False

# Always import pyttsx3 for fallback
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    print("Warning: pyttsx3 not available either!")
    PYTTSX3_AVAILABLE = False

# For audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    try:
        import playsound
        PLAYSOUND_AVAILABLE = True
        PYGAME_AVAILABLE = False
    except ImportError:
        print("Warning: No audio playback library found. Install pygame or playsound for audio playback.")
        PYGAME_AVAILABLE = False
        PLAYSOUND_AVAILABLE = False

class TextToSpeech:
    def __init__(self):
        self.is_speaking = False
        self.current_language = "en"  # Default to English
        self.exaggeration = 0.5  # Default emotional intensity
        self.cfg_weight = 0.5  # Default CFG weight for generation control
        
        # Initialize the appropriate TTS engine
        if CHATTERBOX_AVAILABLE:
            self._init_chatterbox()
        else:
            self._init_pyttsx3()
        
        # Initialize audio playback
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
    
    def _init_chatterbox(self):
        """Initialize Chatterbox TTS models"""
        try:
            # Determine device (GPU if available, otherwise CPU)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {self.device}")
            
            # Load English model
            print("Loading Chatterbox English TTS model...")
            self.english_model = ChatterboxTTS.from_pretrained(device=self.device)
            
            # Load multilingual model
            print("Loading Chatterbox Multilingual TTS model...")
            try:
                self.multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
            except RuntimeError as e:
                if "CUDA device" in str(e) and self.device == "cpu":
                    print("Multilingual model has CUDA/CPU compatibility issue. Using English model for all languages.")
                    self.multilingual_model = None
                else:
                    raise e
            
            self.engine_type = "chatterbox"
            print("Chatterbox TTS models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading Chatterbox models: {e}")
            print("Falling back to pyttsx3...")
            self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 as fallback"""
        if PYTTSX3_AVAILABLE:
            self.engine = pyttsx3.init()
            self.engine_type = "pyttsx3"
            self.setup_voice()
        else:
            print("Error: No TTS engine available!")
            self.engine_type = "none"
    
    def setup_voice(self):
        """Configure voice properties for pyttsx3"""
        if self.engine_type != "pyttsx3":
            return
            
        try:
            # Get available voices
            voices = self.engine.getProperty('voices')
            
            # Try to find a good English voice
            english_voice = None
            for voice in voices:
                if 'english' in voice.name.lower() or 'en' in voice.id.lower():
                    english_voice = voice
                    break
            
            if english_voice:
                self.engine.setProperty('voice', english_voice.id)
                print(f"Using voice: {english_voice.name}")
            
            # Set speech rate and volume
            self.engine.setProperty('rate', 200)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
        except Exception as e:
            print(f"Voice setup error: {e}")
    
    def speak(self, text, blocking=False, language=None, audio_prompt_path=None, fast_mode=None):
        """
        Convert text to speech
        
        Args:
            text (str): Text to speak
            blocking (bool): If True, wait for speech to complete
            language (str): Language code (e.g., 'en', 'fr', 'zh') for multilingual TTS
            audio_prompt_path (str): Path to reference audio for voice cloning
            fast_mode (bool): If True, use faster generation settings
        """
        if not text:
            return
        
        # Use provided language or default
        lang = language or self.current_language
        
        # Auto-enable fast mode for short responses
        if fast_mode is None:
            fast_mode = len(text) < 100  # Fast mode for responses under 100 chars
        
        if blocking:
            self._speak_blocking(text, lang, audio_prompt_path, fast_mode)
        else:
            # Speak in separate thread to avoid blocking GUI
            threading.Thread(
                target=self._speak_blocking, 
                args=(text, lang, audio_prompt_path, fast_mode), 
                daemon=True
            ).start()
    
    def _speak_blocking(self, text, language="en", audio_prompt_path=None, fast_mode=False):
        """Internal method to speak text (blocking)"""
        try:
            self.is_speaking = True
            mode_indicator = "⚡" if fast_mode else "🔊"
            print(f"{mode_indicator} Generating speech ({language}): {text}")
            
            if self.engine_type == "chatterbox":
                self._speak_chatterbox(text, language, audio_prompt_path, fast_mode)
            else:
                self._speak_pyttsx3(text)
                
        except Exception as e:
            print(f"TTS error: {e}")
        finally:
            self.is_speaking = False
            print("🔇 Speech completed")
    
    def _speak_chatterbox(self, text, language="en", audio_prompt_path=None, fast_mode=False):
        """Generate and play speech using Chatterbox TTS (optimized)"""
        try:
            if fast_mode:
                # Ultra-fast settings for short responses
                exaggeration = 0.5  # Minimal emotion for speed
                cfg_weight = 0.8    # Higher CFG for faster generation
                temperature = 0.4   # Very low temperature
                repetition_penalty = 1.2
            else:
                # Balanced settings
                exaggeration = min(self.exaggeration, 1.0)
                cfg_weight = max(self.cfg_weight, 0.7)
                temperature = 0.6
                repetition_penalty = 1.1
            
            # Choose the appropriate model
            if language == "en" or self.multilingual_model is None:
                model = self.english_model
                wav = model.generate(
                    text, 
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight,
                    temperature=temperature,
                    repetition_penalty=repetition_penalty
                )
            else:
                model = self.multilingual_model
                wav = model.generate(
                    text, 
                    language_id=language,
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight,
                    temperature=temperature,
                    repetition_penalty=repetition_penalty
                )
            
            # Save to temporary file and play
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                ta.save(temp_path, wav, model.sr)
            
            # Play the audio
            self._play_audio(temp_path)
            
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
                
        except Exception as e:
            print(f"Chatterbox TTS error: {e}")
            # Fallback to pyttsx3 if available
            if hasattr(self, 'engine'):
                self._speak_pyttsx3(text)
    
    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3 fallback"""
        try:
            # Stop any current speech
            self.engine.stop()
            
            # Speak the text
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"pyttsx3 TTS error: {e}")
            # Try reinitializing engine if run loop error
            if "run loop already started" in str(e):
                try:
                    self.engine = pyttsx3.init()
                    self.setup_voice()
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e2:
                    print(f"pyttsx3 reinit error: {e2}")
    
    def _play_audio(self, audio_path):
        """Play audio file using available audio library"""
        try:
            print(f"Playing audio: {audio_path}")
            if PYGAME_AVAILABLE:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                print("Started pygame playback...")
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                print("Pygame playback completed.")
            elif PLAYSOUND_AVAILABLE:
                from playsound import playsound
                print("Using playsound...")
                playsound(audio_path)
                print("Playsound completed.")
            else:
                print(f"Audio generated but no playback library available: {audio_path}")
        except Exception as e:
            print(f"Audio playback error: {e}")
    
    def stop(self):
        """Stop current speech"""
        try:
            if self.engine_type == "chatterbox":
                if PYGAME_AVAILABLE:
                    pygame.mixer.music.stop()
            else:
                self.engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"Error stopping TTS: {e}")
    
    def set_language(self, language_code):
        """Set default language for TTS"""
        self.current_language = language_code
        print(f"Language set to: {language_code}")
    
    def set_exaggeration(self, exaggeration):
        """Set emotional intensity (0.5-2.0, default 0.5)"""
        self.exaggeration = max(0.5, min(2.0, exaggeration))
        print(f"Exaggeration set to: {self.exaggeration}")
    
    def set_cfg_weight(self, cfg_weight):
        """Set CFG weight for generation control (0.0-1.0, default 0.5)"""
        self.cfg_weight = max(0.0, min(1.0, cfg_weight))
        print(f"CFG weight set to: {self.cfg_weight}")
    
    def set_cfg(self, cfg):
        """Legacy method - maps to cfg_weight for backward compatibility"""
        # Map old cfg range (0.1-2.0) to new cfg_weight range (0.0-1.0)
        mapped_weight = max(0.0, min(1.0, cfg / 2.0))
        self.set_cfg_weight(mapped_weight)
    
    def set_rate(self, rate):
        """Set speech rate (for pyttsx3 fallback only)"""
        if self.engine_type == "pyttsx3":
            try:
                self.engine.setProperty('rate', rate)
            except Exception as e:
                print(f"Error setting rate: {e}")
        else:
            print("Rate setting not applicable for Chatterbox TTS. Use set_cfg() instead.")
    
    def set_volume(self, volume):
        """Set speech volume (for pyttsx3 fallback only)"""
        if self.engine_type == "pyttsx3":
            try:
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            except Exception as e:
                print(f"Error setting volume: {e}")
        else:
            print("Volume setting not applicable for Chatterbox TTS.")
    
    def get_voices(self):
        """Get list of available voices/languages"""
        if self.engine_type == "chatterbox":
            return [
                ("en", "English (Chatterbox)"),
                ("fr", "French (Chatterbox)"),
                ("es", "Spanish (Chatterbox)"),
                ("de", "German (Chatterbox)"),
                ("it", "Italian (Chatterbox)"),
                ("pt", "Portuguese (Chatterbox)"),
                ("ru", "Russian (Chatterbox)"),
                ("ja", "Japanese (Chatterbox)"),
                ("ko", "Korean (Chatterbox)"),
                ("zh", "Chinese (Chatterbox)"),
                ("hi", "Hindi (Chatterbox)"),
                ("ar", "Arabic (Chatterbox)"),
                ("tr", "Turkish (Chatterbox)"),
                ("sw", "Swahili (Chatterbox)")
            ]
        else:
            try:
                voices = self.engine.getProperty('voices')
                return [(voice.id, voice.name) for voice in voices]
            except Exception as e:
                print(f"Error getting voices: {e}")
                return []
    
    def set_voice(self, voice_id):
        """Set voice by ID (language code for Chatterbox)"""
        if self.engine_type == "chatterbox":
            self.set_language(voice_id)
        else:
            try:
                self.engine.setProperty('voice', voice_id)
            except Exception as e:
                print(f"Error setting voice: {e}")
    
    def speak_multilingual(self, text, language):
        """Convenience method for multilingual speech"""
        self.speak(text, language=language)
    
    def speak_with_emotion(self, text, exaggeration=None, cfg=None):
        """Speak with specific emotional settings"""
        old_exag = self.exaggeration
        old_cfg_weight = self.cfg_weight
        
        if exaggeration is not None:
            self.set_exaggeration(exaggeration)
        if cfg is not None:
            self.set_cfg(cfg)
        
        self.speak(text)
        
        # Restore previous settings
        self.exaggeration = old_exag
        self.cfg_weight = old_cfg_weight
    
    def clone_voice(self, text, reference_audio_path):
        """Speak with voice cloning using reference audio"""
        if self.engine_type == "chatterbox":
            self.speak(text, audio_prompt_path=reference_audio_path)
        else:
            print("Voice cloning not available with pyttsx3. Using default voice.")
            self.speak(text)
    
    def test_speech(self):
        """Test speech functionality"""
        if self.engine_type == "chatterbox":
            test_phrases = [
                ("Hello, I am your advanced AI assistant with Chatterbox TTS!", "en"),
                ("Bonjour, je suis votre assistant IA!", "fr"),
                ("¡Hola, soy tu asistente de IA!", "es"),
                ("你好，我是你的AI助手！", "zh"),
                ("こんにちは、私はあなたのAIアシスタントです！", "ja")
            ]
            
            import random
            phrase, lang = random.choice(test_phrases)
            print(f"Testing {lang}: {phrase}")
            self.speak(phrase, language=lang)
            return phrase
        else:
            test_phrases = [
                "Hello, I am your AI assistant using pyttsx3.",
                "Text to speech is working correctly.",
                "This is a test of the speech synthesis system."
            ]
            
            import random
            phrase = random.choice(test_phrases)
            self.speak(phrase)
            return phrase
    
    def get_engine_info(self):
        """Get information about the current TTS engine"""
        if self.engine_type == "chatterbox":
            return {
                "engine": "Chatterbox TTS",
                "device": self.device,
                "multilingual": True,
                "voice_cloning": True,
                "emotion_control": True,
                "languages": len(self.get_voices())
            }
        else:
            return {
                "engine": "pyttsx3",
                "device": "CPU",
                "multilingual": False,
                "voice_cloning": False,
                "emotion_control": False,
                "languages": len(self.get_voices())
            }
    
    def cleanup(self):
        """Clean up TTS resources"""
        try:
            self.stop()
            if PYGAME_AVAILABLE:
                pygame.mixer.quit()
        except Exception as e:
            print(f"TTS cleanup error: {e}")