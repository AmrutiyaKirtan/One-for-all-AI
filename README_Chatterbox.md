# AI Assistant with Chatterbox TTS Integration

This project has been upgraded to use **Chatterbox TTS**, a state-of-the-art text-to-speech model that provides:

- 🌍 **23 languages** out of the box
- 🎭 **Emotion control** (0.5-2.0 intensity)
- 🎯 **Zero-shot voice cloning**
- ⚡ **Ultra-fast inference** (sub-200ms possible)
- 🔊 **Superior quality** vs. traditional TTS

## Quick Start

### 1. Install Chatterbox TTS
```bash
# Run the automated installer
python install_chatterbox.py

# Or install manually
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install chatterbox-tts pygame
```

### 2. Setup Hugging Face Authentication
Chatterbox TTS requires authentication:
```bash
# Run the setup script
python setup_huggingface.py

# Or setup manually:
# 1. Create account at https://huggingface.co/join
# 2. Accept license at https://huggingface.co/ResembleAI/chatterbox
# 3. Create token at https://huggingface.co/settings/tokens
# 4. Login: huggingface-cli login
```

### 3. Test the Installation
```bash
python test.py
```

### 4. Run the AI Assistant
```bash
python main.py
```

## Features

### Basic Usage
- **English TTS**: High-quality English speech synthesis
- **Multilingual**: Support for 23 languages including French, Spanish, Chinese, Japanese, Hindi
- **Emotion Control**: Adjust expressiveness from neutral (0.5) to very dramatic (2.0)
- **Speed Control**: Fine-tune speaking pace and naturalness

### Advanced Features
- **Voice Cloning**: Use reference audio to mimic specific voices
- **Real-time Controls**: Adjust language, emotion, and speed from the GUI
- **Fallback Support**: Automatically falls back to pyttsx3 if Chatterbox isn't available
- **GPU Acceleration**: Automatic CUDA support for faster generation

## GUI Controls

The main application now includes:
- **Language Selector**: Choose from 23+ supported languages
- **Emotion Slider**: Control emotional intensity (0.5-2.0)
- **Speed Slider**: Adjust speaking speed and naturalness (0.3-2.0)
- **TTS Info Button**: View engine capabilities and status

## Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| en   | English  | fr   | French   |
| es   | Spanish  | de   | German   |
| it   | Italian  | pt   | Portuguese |
| ru   | Russian  | ja   | Japanese |
| ko   | Korean   | zh   | Chinese  |
| hi   | Hindi    | ar   | Arabic   |
| tr   | Turkish  | sw   | Swahili  |

## API Examples

### Basic Speech
```python
from text_to_speech import TextToSpeech

tts = TextToSpeech()
tts.speak("Hello, world!")
```

### Multilingual Speech
```python
tts.speak("Bonjour le monde!", language="fr")
tts.speak("¡Hola mundo!", language="es")
tts.speak("你好世界！", language="zh")
```

### Emotional Speech
```python
# Neutral
tts.speak_with_emotion("This is normal speech.", exaggeration=0.5)

# Expressive
tts.speak_with_emotion("This is exciting!", exaggeration=1.5)

# Very dramatic
tts.speak_with_emotion("This is incredible!", exaggeration=2.0)
```

### Voice Cloning
```python
tts.clone_voice("Hello in my voice!", "reference_audio.wav")
```

## Performance Tips

### GPU Acceleration
- Install CUDA-enabled PyTorch for 5-10x faster generation
- Run `python install_chatterbox.py` and select GPU support

### Memory Optimization
- Models are loaded once and cached
- Use CPU version if GPU memory is limited
- Close other applications for better performance

### Quality Settings
- **High Quality**: exaggeration=0.7, cfg=0.3 (slower, more natural)
- **Balanced**: exaggeration=0.5, cfg=1.0 (default)
- **Fast**: exaggeration=0.5, cfg=1.5 (faster, less natural)

## Troubleshooting

### Installation Issues
```bash
# If PyTorch installation fails
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# If Chatterbox installation fails
pip install --upgrade pip
pip install chatterbox-tts

# If audio playback doesn't work
pip install pygame  # or playsound
```

### Common Problems
- **No audio output**: Install pygame or playsound
- **Slow generation**: Install GPU version of PyTorch
- **Import errors**: Run `python test.py` to check dependencies
- **Memory errors**: Use CPU version or close other applications

## Architecture

The TTS system uses a layered approach:
1. **Chatterbox TTS**: Primary high-quality engine
2. **pyttsx3 Fallback**: Backup for compatibility
3. **Audio Playback**: pygame (preferred) or playsound
4. **Thread Safety**: Non-blocking speech generation

## Contributing

To add new features:
1. Extend `TextToSpeech` class in `text_to_speech.py`
2. Update GUI controls in `main.py`
3. Add tests in `test.py`
4. Update this README

## License

This project uses Chatterbox TTS under the MIT license. See individual package licenses for details.