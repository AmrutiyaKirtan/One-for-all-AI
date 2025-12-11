#!/usr/bin/env python3
"""
AI Assistant - Phase 1
Cross-platform AI assistant with voice recognition and text-to-speech
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
from datetime import datetime
import sys
import os

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

# Load environment variables
load_env_file()

# Import our modules
from voice_recognition import VoiceRecognition
from text_to_speech import TextToSpeech
from command_processor import CommandProcessor

class AIAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Assistant - Phase 1")
        self.root.geometry("800x600")
        
        # Initialize components
        self.voice_recognition = VoiceRecognition()
        self.text_to_speech = TextToSpeech()
        
        # Phase 2: Intelligent Command Processor
        try:
            from intelligent_processor import IntelligentCommandProcessor
            # Try Gemini first, fallback to basic processor
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                self.command_processor = IntelligentCommandProcessor(
                    self.text_to_speech, 
                    llm_type="gemini", 
                    api_key=api_key
                )
                print("✓ Phase 2: Intelligent AI processor loaded")
            else:
                print("⚠️  No GEMINI_API_KEY found, using basic processor")
                from command_processor import CommandProcessor
                self.command_processor = CommandProcessor(self.text_to_speech)
        except ImportError:
            print("⚠️  Intelligent processor not available, using basic processor")
            from command_processor import CommandProcessor
            self.command_processor = CommandProcessor(self.text_to_speech)
        
        # GUI state
        self.is_listening = False
        
        # Message queue for thread communication
        self.message_queue = queue.Queue()
        
        self.setup_gui()
        self.setup_callbacks()
        self.process_queue()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="AI Assistant - Phase 1", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Status
        self.status_var = tk.StringVar(value="Ready to start")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Arial", 12))
        status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Action feedback (for silent commands)
        self.action_var = tk.StringVar(value="")
        self.action_label = ttk.Label(main_frame, textvariable=self.action_var, 
                                     font=("Arial", 10), foreground="green")
        self.action_label.grid(row=1, column=0, columnspan=3, pady=(25, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        self.start_btn = ttk.Button(button_frame, text="Start Listening", 
                                   command=self.start_listening)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Listening", 
                                  command=self.stop_listening, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.test_tts_btn = ttk.Button(button_frame, text="Test TTS", 
                                      command=self.test_tts)
        self.test_tts_btn.grid(row=0, column=2, padx=(0, 10))
        
        # TTS Engine info button
        self.engine_info_btn = ttk.Button(button_frame, text="TTS Info", 
                                         command=self.show_engine_info)
        self.engine_info_btn.grid(row=0, column=3)
        
        # TTS Controls
        tts_frame = ttk.LabelFrame(main_frame, text="TTS Controls", padding="10")
        tts_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Language selection
        ttk.Label(tts_frame, text="Language:").grid(row=0, column=0, sticky=tk.W)
        self.language_var = tk.StringVar(value="en")
        self.language_combo = ttk.Combobox(tts_frame, textvariable=self.language_var, 
                                          width=15, state="readonly")
        self.language_combo.grid(row=0, column=1, padx=(5, 20))
        self.update_language_options()
        
        # Emotion control
        ttk.Label(tts_frame, text="Emotion:").grid(row=0, column=2, sticky=tk.W)
        self.emotion_var = tk.DoubleVar(value=0.5)
        self.emotion_scale = ttk.Scale(tts_frame, from_=0.5, to=2.0, 
                                      variable=self.emotion_var, orient=tk.HORIZONTAL)
        self.emotion_scale.grid(row=0, column=3, padx=(5, 20), sticky=(tk.W, tk.E))
        
        # Speed control
        ttk.Label(tts_frame, text="Speed:").grid(row=0, column=4, sticky=tk.W)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(tts_frame, from_=0.3, to=2.0, 
                                    variable=self.speed_var, orient=tk.HORIZONTAL)
        self.speed_scale.grid(row=0, column=5, padx=(5, 0), sticky=(tk.W, tk.E))
        
        tts_frame.columnconfigure(3, weight=1)
        tts_frame.columnconfigure(5, weight=1)
        
        # Text input as fallback
        text_input_frame = ttk.Frame(main_frame)
        text_input_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(text_input_frame, text="Or type command:").grid(row=0, column=0, sticky=tk.W)
        
        self.text_input = ttk.Entry(text_input_frame, width=50)
        self.text_input.grid(row=1, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        self.text_input.bind('<Return>', self.process_text_input)
        
        send_btn = ttk.Button(text_input_frame, text="Send", command=self.process_text_input)
        send_btn.grid(row=1, column=1)
        
        text_input_frame.columnconfigure(0, weight=1)
        
        # Transcript area
        transcript_label = ttk.Label(main_frame, text="Transcript:", 
                                   font=("Arial", 12, "bold"))
        transcript_label.grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        self.transcript_text = scrolledtext.ScrolledText(main_frame, 
                                                        height=10, width=70)
        self.transcript_text.grid(row=6, column=0, columnspan=3, 
                                 pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Commands history
        commands_label = ttk.Label(main_frame, text="Command History:", 
                                  font=("Arial", 12, "bold"))
        commands_label.grid(row=7, column=0, sticky=tk.W, pady=(0, 5))
        
        self.commands_text = scrolledtext.ScrolledText(main_frame, 
                                                      height=8, width=70)
        self.commands_text.grid(row=8, column=0, columnspan=3, 
                               sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        main_frame.rowconfigure(8, weight=1)
    
    def setup_callbacks(self):
        # Set up voice recognition callbacks
        self.voice_recognition.set_callbacks(
            on_result=self.on_voice_result,
            on_error=self.on_voice_error,
            on_start=self.on_voice_start,
            on_stop=self.on_voice_stop
        )
        
        # Keyboard shortcuts
        self.root.bind('<Control-space>', lambda e: self.toggle_listening())
        self.root.bind('<Escape>', lambda e: self.stop_listening())
    
    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            
            # Start voice recognition in separate thread
            threading.Thread(target=self.voice_recognition.start_listening, 
                           daemon=True).start()
    
    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.voice_recognition.stop_listening()
    
    def toggle_listening(self):
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def update_language_options(self):
        """Update language dropdown with available options"""
        voices = self.text_to_speech.get_voices()
        languages = [voice[0] for voice in voices]
        self.language_combo['values'] = languages
        if languages:
            self.language_combo.set(languages[0])
    
    def show_engine_info(self):
        """Show TTS engine information"""
        info = self.text_to_speech.get_engine_info()
        info_text = f"""TTS Engine Information:
        
Engine: {info['engine']}
Device: {info['device']}
Multilingual: {info['multilingual']}
Voice Cloning: {info['voice_cloning']}
Emotion Control: {info['emotion_control']}
Available Languages: {info['languages']}
        """
        
        # Create info window
        info_window = tk.Toplevel(self.root)
        info_window.title("TTS Engine Info")
        info_window.geometry("400x300")
        
        text_widget = scrolledtext.ScrolledText(info_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
    
    def test_tts(self):
        """Test TTS with current settings"""
        # Get current settings
        language = self.language_var.get()
        exaggeration = self.emotion_var.get()
        cfg = self.speed_var.get()
        
        # Apply settings to TTS
        self.text_to_speech.set_language(language)
        self.text_to_speech.set_exaggeration(exaggeration)
        self.text_to_speech.set_cfg(cfg)
        
        # Test phrase
        phrase = self.text_to_speech.test_speech()
        self.add_to_transcript(f"TTS Test ({language}, emotion={exaggeration:.1f}, speed={cfg:.1f}): {phrase}")
    
    def process_text_input(self, event=None):
        """Process text input as command"""
        text = self.text_input.get().strip()
        if text:
            self.text_input.delete(0, tk.END)
            
            # Apply current TTS settings
            language = self.language_var.get()
            exaggeration = self.emotion_var.get()
            cfg = self.speed_var.get()
            
            self.text_to_speech.set_language(language)
            self.text_to_speech.set_exaggeration(exaggeration)
            self.text_to_speech.set_cfg(cfg)
            
            self.add_to_transcript(f"You (text): {text}")
            
            # Check if it's a silent command
            if hasattr(self.command_processor, 'is_silent_command') and self.command_processor.is_silent_command(text):
                # Show immediate visual feedback
                self.action_var.set("Executing...")
                self.root.update()
                
                # Process command silently
                response = self.command_processor.process_command(text)
                
                # Show result briefly
                if response:
                    self.action_var.set(f"✓ {response}")
                    self.root.after(3000, lambda: self.action_var.set(""))  # Clear after 3 seconds
                    self.add_to_commands(f"{datetime.now().strftime('%H:%M:%S')}: {text}")
                    self.add_to_transcript(f"Assistant: {response}")
            else:
                # Show "thinking" indicator for AI commands
                self.action_var.set("🤖 Thinking...")
                self.root.update()
                
                # Process command (with TTS)
                response = self.command_processor.process_command(text)
                
                if response:
                    # Show text response immediately
                    self.add_to_commands(f"{datetime.now().strftime('%H:%M:%S')}: {text}")
                    self.add_to_transcript(f"Assistant: {response}")
                    
                    # Show voice generation status
                    self.action_var.set("🔊 Speaking...")
                    self.root.update()
                    
                    # Clear status after estimated speech time
                    estimated_time = len(response) * 50  # ~50ms per character
                    self.root.after(estimated_time, lambda: self.action_var.set(""))
    
    def on_voice_result(self, text):
        self.message_queue.put(('transcript', text))
        self.message_queue.put(('command', text))
    
    def on_voice_error(self, error):
        self.message_queue.put(('error', f"Voice recognition error: {error}"))
    
    def on_voice_start(self):
        self.message_queue.put(('status', 'Listening...'))
    
    def on_voice_stop(self):
        self.message_queue.put(('status', 'Stopped listening'))
    
    def process_queue(self):
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                
                if msg_type == 'transcript':
                    self.add_to_transcript(f"You: {data}")
                elif msg_type == 'command':
                    response = self.command_processor.process_command(data)
                    if response:
                        self.add_to_commands(f"{datetime.now().strftime('%H:%M:%S')}: {data}")
                        self.add_to_transcript(f"Assistant: {response}")
                elif msg_type == 'status':
                    self.status_var.set(data)
                elif msg_type == 'error':
                    self.status_var.set(data)
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_queue)
    
    def add_to_transcript(self, text):
        self.transcript_text.insert(tk.END, f"{text}\n")
        self.transcript_text.see(tk.END)
    
    def add_to_commands(self, text):
        self.commands_text.insert(tk.END, f"{text}\n")
        self.commands_text.see(tk.END)
    
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            self.voice_recognition.cleanup()
            self.text_to_speech.cleanup()

def main():
    print("Starting AI Assistant...")
    app = AIAssistantGUI()
    app.run()

if __name__ == "__main__":
    main()