#!/usr/bin/env python3
"""
Intelligent Command Processor for Phase 2
Combines local commands with LLM-powered responses
"""

import re
import json
import os
from datetime import datetime
import platform
import psutil
from system_control import SystemController

# Try to import LLM libraries
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class ConversationContext:
    """Manages conversation history and context"""
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
        self.user_preferences = {}
    
    def add_exchange(self, user_input, assistant_response):
        """Add a conversation exchange to history"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'assistant': assistant_response
        })
        
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context_summary(self):
        """Get a summary of recent conversation for LLM context"""
        if not self.history:
            return ""
        
        recent = self.history[-3:]  # Last 3 exchanges
        context = "Recent conversation:\n"
        for exchange in recent:
            context += f"User: {exchange['user']}\n"
            context += f"Assistant: {exchange['assistant']}\n"
        return context

class LocalCommandHandler:
    """Handles simple commands locally without LLM"""
    def __init__(self):
        self.system_controller = SystemController()
        self.local_patterns = {
            # Folder operations (prioritize these to avoid greeting conflicts)
            r'\bcreate\s+folder\s+(.+?)(?:\s+(?:in|inside|on)\s+(.+))$': self.create_folder_advanced,
            r'\bmake\s+folder\s+(.+?)(?:\s+(?:in|inside|on)\s+(.+))$': self.create_folder_advanced,
            r'\bcreate\s+folder\s+([\w\s]+)': self.create_folder,
            r'\bmake\s+folder\s+([\w\s]+)': self.create_folder,
            r'\bnew\s+folder\s+([\w\s]+)': self.create_folder,
            
            # System control
            r'\bopen\s+(\w+)': self.open_app,
            r'\bclose\s+(\w+)': self.close_app,
            r'\bvolume\s+(\d+)': self.set_volume,
            r'\bset\s+volume\s+(\d+)': self.set_volume,
            r'\bincrease\s+volume': self.increase_volume,
            r'\bdecrease\s+volume': self.decrease_volume,
            r'\bvolume\s+up': self.increase_volume,
            r'\bvolume\s+down': self.decrease_volume,
            r'\block\s+(computer|pc)': self.lock_computer,
            r'\bshutdown\s+(computer|pc)': self.shutdown_computer,
            r'\brunning\s+(apps|applications)': self.get_running_apps,
            
            # Time and date
            r'\b(time|clock)\b': self.get_time,
            r'\b(date|today)\b': self.get_date,
            
            # System info
            r'\b(system|computer|pc)\s+(info|information|stats)\b': self.get_system_info,
            r'\b(cpu|processor)\s+(usage|load)\b': self.get_cpu_usage,
            r'\b(memory|ram)\s+(usage|info)\b': self.get_memory_info,
            
            # Simple calculations
            r'\b(\d+)\s*[\+\-\*\/]\s*(\d+)\b': self.simple_math,
            
            # Greetings (put these last to avoid conflicts)
            r'^(hello|hi|hey)$': self.greeting,
            r'^(goodbye|bye|exit|quit)$': self.farewell,
        }
    
    def can_handle(self, text):
        """Check if this command can be handled locally"""
        text_lower = text.lower()
        for pattern in self.local_patterns:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def execute(self, text):
        """Execute local command"""
        text_lower = text.lower()
        for pattern, handler in self.local_patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                try:
                    return handler(match, text)
                except Exception as e:
                    return f"Error executing command: {e}"
        
        return "Command not recognized locally"
    
    def get_time(self, match, original_text):
        """Get current time"""
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}"
    
    def get_date(self, match, original_text):
        """Get current date"""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"
    
    def get_system_info(self, match, original_text):
        """Get system information"""
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        return f"You're running {system} {release} on {machine} architecture"
    
    def get_cpu_usage(self, match, original_text):
        """Get CPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        return f"Current CPU usage is {cpu_percent}%"
    
    def get_memory_info(self, match, original_text):
        """Get memory information"""
        memory = psutil.virtual_memory()
        used_gb = memory.used / (1024**3)
        total_gb = memory.total / (1024**3)
        return f"Memory usage: {used_gb:.1f}GB of {total_gb:.1f}GB ({memory.percent}%)"
    
    def greeting(self, match, original_text):
        """Handle greetings"""
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm ready to assist you.",
        ]
        import random
        return random.choice(greetings)
    
    def farewell(self, match, original_text):
        """Handle farewells"""
        farewells = [
            "Goodbye! Have a great day!",
            "See you later!",
            "Take care!",
        ]
        import random
        return random.choice(farewells)
    
    def simple_math(self, match, original_text):
        """Handle simple math operations"""
        try:
            # Extract the math expression
            math_match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', original_text)
            if math_match:
                num1 = int(math_match.group(1))
                operator = math_match.group(2)
                num2 = int(math_match.group(3))
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "Cannot divide by zero!"
                    result = num1 / num2
                
                return f"{num1} {operator} {num2} = {result}"
        except:
            pass
        return "I couldn't calculate that"
    
    # System Control Methods
    def open_app(self, match, original_text):
        """Open an application"""
        app_name = match.group(1) if match.groups() else "unknown"
        return self.system_controller.open_application(app_name)
    
    def close_app(self, match, original_text):
        """Close an application"""
        app_name = match.group(1) if match.groups() else "unknown"
        return self.system_controller.close_application(app_name)
    
    def set_volume(self, match, original_text):
        """Set system volume"""
        volume = match.group(1) if match.groups() else "50"
        return self.system_controller.set_volume(volume)
    
    def lock_computer(self, match, original_text):
        """Lock the computer"""
        return self.system_controller.lock_computer()
    
    def shutdown_computer(self, match, original_text):
        """Shutdown the computer"""
        return self.system_controller.shutdown_computer()
    
    def create_folder(self, match, original_text):
        """Create a new folder"""
        folder_name = match.group(1) if match.groups() else "new_folder"
        return self.system_controller.create_folder(folder_name)
    
    def create_folder_advanced(self, match, original_text):
        """Create a folder with optional location specification"""
        folder_name = match.group(1).strip() if match.groups() else "new_folder"
        location = match.group(2).strip() if len(match.groups()) > 1 and match.group(2) else None
        
        # Clean up folder name (remove quotes, handle spaces)
        folder_name = folder_name.replace('"', '').replace("'", "")
        
        if location:
            location = location.replace('"', '').replace("'", "")
            return self.system_controller.create_folder_in_location(folder_name, location)
        else:
            return self.system_controller.create_folder(folder_name)
    
    def get_running_apps(self, match, original_text):
        """Get running applications"""
        return self.system_controller.get_running_apps()
    
    def increase_volume(self, match, original_text):
        """Increase system volume"""
        return self.system_controller.adjust_volume("+10")
    
    def decrease_volume(self, match, original_text):
        """Decrease system volume"""
        return self.system_controller.adjust_volume("-10")

class GeminiHandler:
    """Google Gemini LLM integration"""
    def __init__(self, api_key=None):
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI library not available")
        
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_response(self, user_input, context=""):
        """Get intelligent response from Gemini"""
        system_prompt = """You are a helpful AI assistant. Respond naturally and concisely.
        Keep responses under 100 words unless specifically asked for more detail.
        Be friendly, informative, and helpful."""
        
        full_prompt = f"{system_prompt}\n\n{context}\nUser: {user_input}\nAssistant:"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            return f"I'm having trouble thinking right now. Error: {e}"

class OllamaHandler:
    """Local Ollama LLM integration"""
    def __init__(self, model="llama3.1:8b", base_url="http://localhost:11434"):
        if not OLLAMA_AVAILABLE:
            raise ImportError("Requests library not available for Ollama")
        
        self.model = model
        self.base_url = base_url
    
    def is_available(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_response(self, user_input, context=""):
        """Get response from local Ollama model"""
        if not self.is_available():
            return "Local AI model is not available. Please start Ollama."
        
        system_prompt = "You are a helpful AI assistant. Respond naturally and concisely."
        full_prompt = f"{system_prompt}\n\n{context}\nUser: {user_input}\nAssistant:"
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 150
                }
            }, timeout=30)
            
            if response.status_code == 200:
                return response.json()["response"].strip()
            else:
                return "I'm having trouble with the local AI model."
        except Exception as e:
            return f"Local AI error: {e}"

class IntelligentCommandProcessor:
    """Main intelligent command processor combining local and LLM responses"""
    def __init__(self, text_to_speech, llm_type="gemini", api_key=None):
        self.tts = text_to_speech
        self.local_handler = LocalCommandHandler()
        self.context = ConversationContext()
        
        # Commands that should execute silently (no TTS delay)
        self.silent_commands = {
            'open', 'close', 'volume', 'increase volume', 'decrease volume',
            'volume up', 'volume down', 'lock', 'shutdown', 
            'create folder', 'make folder', 'new folder', 'running apps'
        }
        
        # Initialize LLM handler
        self.llm_handler = None
        if llm_type == "gemini" and GEMINI_AVAILABLE:
            try:
                self.llm_handler = GeminiHandler(api_key)
                print("✓ Gemini AI initialized")
            except Exception as e:
                print(f"✗ Gemini initialization failed: {e}")
        
        elif llm_type == "ollama" and OLLAMA_AVAILABLE:
            try:
                self.llm_handler = OllamaHandler()
                if self.llm_handler.is_available():
                    print("✓ Ollama AI initialized")
                else:
                    print("✗ Ollama not running")
                    self.llm_handler = None
            except Exception as e:
                print(f"✗ Ollama initialization failed: {e}")
    
    def is_silent_command(self, text):
        """Check if command should execute silently"""
        text_lower = text.lower()
        return any(cmd in text_lower for cmd in self.silent_commands)
    
    def process_command(self, text):
        """Process command with intelligent response"""
        if not text.strip():
            return
        
        print(f"Processing: {text}")
        is_silent = self.is_silent_command(text)
        
        # Try local commands first (fast and free)
        if self.local_handler.can_handle(text):
            response = self.local_handler.execute(text)
            print(f"Local response: {response}")
            
            # For system commands, show response but don't speak it
            if is_silent:
                print(f"✓ {response} (silent execution)")
                # Add to history but don't speak
                self.context.add_exchange(text, response)
                return response
        
        # Use LLM for complex queries
        elif self.llm_handler:
            print("🤖 Generating AI response...")
            context = self.context.get_context_summary()
            response = self.llm_handler.get_response(text, context)
            print(f"AI response: {response}")
        
        # Fallback to simple echo
        else:
            response = f"I heard you say: {text}. I don't have AI capabilities enabled right now."
            print(f"Fallback response: {response}")
        
        # Add to conversation history
        self.context.add_exchange(text, response)
        
        # Start voice generation immediately (non-blocking)
        if self.tts and not is_silent:
            print("🔊 Starting voice generation...")
            self.tts.speak(response, blocking=False)  # Non-blocking
        
        return response
    
    def get_capabilities(self):
        """Get information about current capabilities"""
        capabilities = {
            "local_commands": True,
            "llm_available": self.llm_handler is not None,
            "llm_type": type(self.llm_handler).__name__ if self.llm_handler else None,
            "conversation_memory": True
        }
        return capabilities