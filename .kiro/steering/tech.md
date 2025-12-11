# Technology Stack & Development Guide

## Core Technologies

### Language & Framework
- **Python 3.7+**: Core application language
- **tkinter**: Cross-platform GUI framework (included with Python)
- **Threading**: Non-blocking operations for voice/audio processing

### AI & Voice Processing
- **Chatterbox TTS**: Primary neural text-to-speech engine
  - 23+ languages, emotion control, voice cloning
  - PyTorch + torchaudio backend
  - Hugging Face model distribution
- **SpeechRecognition**: Voice input processing
  - Google Speech API (cloud-based, requires internet)
  - PyAudio for microphone access
- **pyttsx3**: Fallback TTS engine (system voices)

### Audio Processing
- **pygame**: Primary audio playback (preferred)
- **playsound**: Fallback audio playback
- **PyAudio**: Microphone input (requires system dependencies)

## Dependencies

### Core Requirements
```
speechrecognition>=3.10.0
pyttsx3>=2.90
torch>=2.0.0
torchaudio>=2.0.0
chatterbox-tts
pygame>=2.0.0
```

### Installation Commands

#### Basic Setup
```bash
pip install -r requirements.txt
```

#### Advanced TTS Setup
```bash
# Install Chatterbox TTS dependencies
python install_chatterbox.py

# Setup Hugging Face authentication
python setup_huggingface.py
```

#### PyAudio Installation (Platform-Specific)
```bash
# Windows
pip install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux (Ubuntu/Debian)
sudo apt-get install python3-pyaudio
# or
sudo apt-get install portaudio19-dev python3-all-dev
pip install pyaudio
```

## Build & Test Commands

### Running the Application
```bash
python main.py
```

### Testing Components
```bash
# Test all TTS features (multilingual, emotion, voice cloning)
python test.py

# Test basic functionality
python -c "import speech_recognition; import pyttsx3; print('Basic dependencies OK')"

# Test Chatterbox TTS
python -c "from chatterbox.tts import ChatterboxTTS; print('Chatterbox TTS OK')"
```

### Development Tools
```bash
# Debug Chatterbox model loading
python debug_chatterbox.py

# Package for distribution
pip install pyinstaller
pyinstaller --onefile main.py
```

## Architecture Patterns

### Modular Design
- **Separation of Concerns**: Each module handles one responsibility
- **Dependency Injection**: TTS engine passed to CommandProcessor
- **Callback Pattern**: Voice recognition events handled via callbacks

### Threading Model
- **Main Thread**: GUI updates and user interactions
- **Voice Thread**: Continuous audio processing
- **TTS Threads**: Non-blocking speech synthesis
- **Queue-based Communication**: Thread-safe message passing

### Fallback Architecture
- **Graceful Degradation**: Chatterbox TTS → pyttsx3 → text-only
- **Error Handling**: Comprehensive exception management
- **Resource Management**: Proper cleanup and resource disposal