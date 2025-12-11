# Project Structure & Organization

## Root Directory Layout

```
ai-assistant/
├── main.py                    # Main application entry point & GUI
├── voice_recognition.py       # Speech-to-text functionality
├── text_to_speech.py         # Neural TTS with Chatterbox integration
├── command_processor.py      # Command parsing and execution
├── test.py                   # Comprehensive testing suite
├── project_log.md            # Development history and decisions
├── README.md                 # Basic project documentation
├── README_Chatterbox.md      # Advanced TTS integration guide
├── requirements.txt          # Core Python dependencies
├── requirements_chatterbox.txt # Advanced TTS dependencies
├── setup.py                  # Package configuration
├── install_chatterbox.py     # Automated TTS installation
├── install_pyaudio.py        # PyAudio installation helper
├── setup_huggingface.py      # HF authentication setup
├── voice_recognition_windows.py # Windows-specific voice handling
├── .venv/                    # Virtual environment
├── __pycache__/              # Python bytecode cache
└── .kiro/                    # Kiro IDE configuration
    └── steering/             # AI assistant guidance rules
```

## Core Module Architecture

### Application Layer (`main.py`)
- **AIAssistantGUI**: Main application controller
- **GUI Components**: tkinter interface, event handling
- **Thread Coordination**: Message queue for cross-thread communication
- **User Interactions**: Button handlers, keyboard shortcuts, text input

### Voice Processing Layer
- **`voice_recognition.py`**: Speech-to-text using SpeechRecognition library
- **`text_to_speech.py`**: Dual-engine TTS (Chatterbox neural + pyttsx3 fallback)
- **Audio Pipeline**: Microphone input → Recognition → Command processing → TTS output

### Command Processing Layer
- **`command_processor.py`**: Pattern matching and command execution
- **Extensible Commands**: Regex-based pattern matching with action functions
- **Built-in Commands**: Time, date, system info, greetings

## File Naming Conventions

### Python Modules
- **Snake case**: `voice_recognition.py`, `text_to_speech.py`
- **Descriptive names**: Files clearly indicate their primary function
- **Single responsibility**: Each module handles one major component

### Installation Scripts
- **Prefix pattern**: `install_*.py` for setup automation
- **Setup pattern**: `setup_*.py` for configuration tasks

### Documentation
- **README pattern**: `README.md` (basic), `README_Chatterbox.md` (specific feature)
- **Requirements pattern**: `requirements.txt` (core), `requirements_chatterbox.txt` (feature-specific)

## Code Organization Patterns

### Class Structure
- **Single class per module**: Each Python file contains one primary class
- **Dependency injection**: External dependencies passed to constructors
- **Callback patterns**: Event-driven communication between modules

### Method Naming
- **Public methods**: Clear, action-oriented names (`start_listening`, `process_command`)
- **Private methods**: Underscore prefix (`_speak_blocking`, `_init_chatterbox`)
- **Callback methods**: `on_*` prefix for event handlers (`on_voice_result`)

### Configuration Management
- **Environment variables**: Sensitive data (API keys) via environment
- **Class attributes**: Default settings as instance variables
- **Runtime configuration**: GUI controls for user preferences

## Extension Points

### Adding New Commands
```python
# In command_processor.py
processor.add_custom_command(
    name="weather",
    patterns=[r'\b(weather|temperature)\b'],
    action=get_weather_function
)
```

### Adding New TTS Engines
- Extend `TextToSpeech` class with new `_speak_*` methods
- Add engine detection in `__init__`
- Update fallback chain in `_speak_blocking`

### GUI Extensions
- Add new controls in `setup_gui()` method
- Create corresponding event handlers
- Update message queue processing for new events

## Development Workflow

### Local Development
1. **Virtual Environment**: Use `.venv/` for isolated dependencies
2. **Testing**: Run `python test.py` for comprehensive validation
3. **Debugging**: Use `debug_chatterbox.py` for TTS troubleshooting

### Adding Features
1. **Module Creation**: Create new `.py` file following naming conventions
2. **Integration**: Import and instantiate in `main.py`
3. **Testing**: Add test cases to `test.py`
4. **Documentation**: Update relevant README files