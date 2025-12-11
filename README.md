# AI Assistant - Phase 1

A cross-platform AI assistant with voice recognition and text-to-speech capabilities, designed to handle complex multi-layered tasks.

## Features

- **Voice Recognition**: Continuous speech recognition using Google's speech API
- **Text-to-Speech**: Cross-platform speech synthesis
- **Command Processing**: Extensible command system with pattern matching
- **GUI Interface**: User-friendly tkinter interface
- **Cross-platform**: Runs on Windows, macOS, and Linux

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install PyAudio (required for microphone access):**
   
   **Windows:**
   ```bash
   pip install pyaudio
   ```
   
   **macOS:**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install python3-pyaudio
   # or
   sudo apt-get install portaudio19-dev python3-all-dev
   pip install pyaudio
   ```

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Using the interface:**
   - Click "Start Listening" to begin voice recognition
   - Use "Test TTS" to verify text-to-speech functionality
   - Keyboard shortcuts:
     - `Ctrl+Space`: Toggle listening
     - `Escape`: Stop listening

3. **Voice Commands:**
   - "Hello" / "Hi" - Greeting
   - "What time is it?" - Current time
   - "What's the date?" - Current date
   - "System info" - Basic system information
   - "Goodbye" - Farewell

## Project Structure

```
ai-assistant/
├── main.py              # Main application entry point
├── voice_recognition.py # Speech-to-text functionality
├── text_to_speech.py   # Text-to-speech functionality
├── command_processor.py # Command parsing and execution
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── project_log.md      # Development log
└── README.md           # This file
```

## Development

### Adding Custom Commands

```python
# In command_processor.py
processor.add_custom_command(
    name="weather",
    patterns=[r'\b(weather|temperature)\b'],
    action=get_weather_function
)
```

### Extending Voice Recognition

The voice recognition module supports various speech recognition engines:
- Google Speech Recognition (default, requires internet)
- Sphinx (offline, less accurate)
- Wit.ai
- Microsoft Bing Voice Recognition
- Houndify API

## Future Enhancements

- [ ] Local AI model integration
- [ ] Mobile app development
- [ ] Advanced task chaining
- [ ] Custom workflow creation
- [ ] Integration with system APIs
- [ ] Plugin system

## Troubleshooting

**Microphone not working:**
- Check microphone permissions
- Ensure PyAudio is properly installed
- Test with `python -c "import pyaudio; print('PyAudio OK')"`

**Speech recognition errors:**
- Check internet connection (Google Speech API requires internet)
- Verify microphone is not being used by other applications

**TTS not working:**
- Check system audio settings
- Verify pyttsx3 installation
- Test with `python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('test'); engine.runAndWait()"`

## License

MIT License - see LICENSE file for details