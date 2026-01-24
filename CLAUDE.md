# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Whisper STT Global** is a Windows voice-to-text transcription service that converts speech to text in real-time and injects it into any active application field. The project uses OpenAI's Whisper models locally for transcription, with support for three engine implementations:

1. **whisper-cpp** (fastest, ~0.2-0.5s latency) - C++ implementation with GGML models
2. **faster-whisper** (fast, ~0.5-2s latency) - Python optimized with Rust dependencies
3. **whisper** (standard, ~2-5s latency) - Reference Python implementation

All processing happens locally (offline after initial model download), with no internet connection required.

## Architecture

### Core Components

The application follows a modular architecture with these key modules:

- **src/main.py**: Main service orchestrator (`WhisperSTTService` class)
  - Manages lifecycle of all components
  - Handles engine fallback chain: whisper-cpp → faster-whisper → whisper
  - Coordinates hotkey callbacks with audio capture and transcription

- **src/audio_capture.py**: Audio recording module
  - Uses `sounddevice` for microphone capture
  - Implements silence detection to auto-stop recording
  - Stores audio in numpy arrays (16kHz mono by default)

- **src/whisper_transcriber.py**: Standard Whisper engine wrapper
- **src/faster_whisper_transcriber.py**: Faster-Whisper engine wrapper
- **src/whisper_cpp_transcriber.py**: Whisper.cpp engine wrapper

- **src/text_injector.py**: Text injection module
  - Uses `pyautogui` and `pyperclip` for clipboard-based injection
  - Alternative `pywin32` direct injection (if clipboard fails)

- **src/keyboard_hotkey.py**: Hotkey management using `pynput`
- **src/notifications.py**: Windows notification system (win10toast/MessageBox fallback)

### Engine Selection & Fallback Logic

The service attempts to load engines in order of performance (main.py:193-255):

```python
engine = config["whisper"]["engine"]  # "whisper-cpp", "faster-whisper", or "whisper"

# Priority chain with automatic fallback:
if engine == "whisper-cpp":
    try: load whisper.cpp
    except: fallback to faster-whisper

if engine == "faster-whisper":
    try: load faster-whisper
    except: fallback to whisper standard

if engine == "whisper":
    load whisper standard (always works)
```

### Configuration System

All settings are in `config.json` (see config.json:1-24):

```json
{
  "whisper": {
    "engine": "faster-whisper",  // whisper-cpp | faster-whisper | whisper
    "model": "medium",            // tiny, base, small, medium, large
    "language": "fr",
    "device": "cpu",              // cpu or cuda
    "compute_type": "int8"        // int8, int16, float16, float32
  },
  "audio": { ... },
  "hotkey": {
    "modifiers": ["ctrl", "alt"],
    "key": "7"
  }
}
```

## Development Commands

### Running the Service

**Primary method** (with dependency checking):
```bash
run_whisper.bat
```

**Alternative** (direct Python execution):
```bash
python -m src.main
```

**From specific directory**:
```bash
cd /mnt/c/programmation/whisper_local_STT
python -m src.main
```

### Installation & Setup

**Full installation** (dependencies + checks):
```bash
scripts/install.bat
```

**Faster-Whisper specific** (requires Rust):
```bash
scripts/install_faster_whisper_complete.bat
```

**Whisper.cpp setup** (C++ engine):
```bash
# Via pip
pip install whisper-cpp-python

# Or from source (for GPU support)
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp && mkdir build && cd build
cmake .. -DWHISPER_CUDA=ON  # for NVIDIA GPUs
make -j && pip install .
```

### Python Version Requirements

- **Recommended**: Python 3.11 or 3.12
- **Minimum**: Python 3.10
- **Avoid**: Python 3.14+ (faster-whisper compilation issues)

Check version:
```bash
python --version
py --list  # shows all installed versions

# Use specific version if multiple are installed
py -3.11 run_whisper.bat
```

### Dependencies

Core dependencies (requirements.txt):
```
openai-whisper>=20231117
faster-whisper>=0.10.0  # requires Rust
torch>=2.0.0
sounddevice>=0.4.6
pyautogui>=0.9.54
pywin32>=306
keyboard>=0.13.5
win10toast  # for notifications
```

Install dependencies:
```bash
pip install -r requirements.txt

# faster-whisper specific (if Rust installed)
pip install faster-whisper

# whisper-cpp specific
pip install whisper-cpp-python
```

### Testing Components

**Test notifications**:
```bash
python test_notifications.py
```

**Test audio capture**:
```python
from src.audio_capture import AudioCapture
capture = AudioCapture()
# Manual test with microphone
```

**Test transcription**:
```python
from src.whisper_transcriber import WhisperTranscriber
transcriber = WhisperTranscriber(model_name="base")
transcriber.load_model()
# Pass audio data to test
```

## Key Implementation Details

### Hotkey Toggle Pattern

The service uses a toggle pattern for recording (main.py:276-289):
```python
def _on_hotkey_pressed():
    if is_recording:
        stop_and_process()  # stops recording, transcribes, injects
    else:
        start_recording()   # begins audio capture
```

User workflow: Press Ctrl+Alt+7 to start → Speak → Press again to stop and transcribe.

### Audio Processing Flow

1. User presses hotkey → `_start_recording()` called
2. `AudioCapture.start_recording()` captures audio chunks
3. User presses hotkey again → `_process_recording()` called
4. `AudioCapture.stop_recording()` returns numpy array
5. Transcriber processes audio → returns text string
6. `TextInjector.inject_text()` pastes to active window

### Notification System

The app shows Windows notifications at each step (main.py:299-363):
- 🎤 Recording started
- ⏳ Processing (transcribing)
- ✅ Text ready (shows first 100 chars)
- ❌ Errors (with error messages)

Notifications use `win10toast` for balloon tips, fallback to `MessageBox` if unavailable.

### Logging

Logs go to:
- Console (stdout)
- File: `whisper_stt.log` (configurable in config.json)

Log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## Common Issues & Solutions

### faster-whisper Installation Failures

Python 3.14+ has Cython compilation issues with faster-whisper:

**Solution 1**: Use Python 3.11/3.12
```bash
py -3.11 run_whisper.bat
```

**Solution 2**: Use whisper-standard instead
```json
{"whisper": {"engine": "whisper"}}  // in config.json
```

**Solution 3**: Force specific version
```bash
pip install faster-whisper==1.2.1 --no-build-isolation
```

### "Module not found" Errors

Ensure PYTHONPATH includes project root:
```bash
# In scripts
set PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%

# Or explicitly
export PYTHONPATH="/mnt/c/programmation/whisper_local_STT:$PYTHONPATH"
```

### No Audio Captured

Check:
1. Windows microphone permissions (Settings > Privacy > Microphone)
2. Default input device (Settings > System > Sound)
3. Test with Windows Voice Recorder app first
4. Adjust `silence_threshold` in config.json (lower = more sensitive)

### Text Not Injecting

Some apps block automated input (security apps, UAC prompts):
- Try running service as Administrator
- Check if clipboard-based injection works (`use_clipboard=True` in TextInjector)
- Manually paste from clipboard as fallback

### GPU/CUDA Errors

"CUDA not available" is normal without NVIDIA GPU. Service works fine on CPU.

For GPU support:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Then set in config.json:
```json
{"whisper": {"device": "cuda"}}
```

## Model Recommendations

| Model | Speed | Accuracy | RAM Usage | Use Case |
|-------|-------|----------|-----------|----------|
| tiny  | Fastest | Low | ~1GB | Quick testing |
| base  | Very fast | Fair | ~1GB | Drafts, notes |
| small | Fast | Good | ~2GB | General use |
| **medium** | Moderate | **Very good** | ~5GB | **Recommended** |
| large | Slow | Best | ~10GB | High accuracy needs |

## Windows Service Setup

To auto-start at boot:
```bash
scripts/install_windows_service.bat  # run as Administrator
```

See `GUIDE_DEMARRAGE_AUTOMATIQUE.md` for details.

## Project-Specific Conventions

- **Language**: French for user-facing messages, English for code/comments
- **Line endings**: Windows (CRLF) for .bat files, LF for Python
- **Python imports**: Absolute imports from `src.` namespace (main.py:20-23)
- **Error handling**: Log with `exc_info=True` for full tracebacks
- **Configuration**: Never hardcode paths/settings, use config.json

## Documentation Files

Core docs in `/doc/outils/`:
- `claude_cli_extensions.md` - Claude Code CLI reference
- `cursor_cli_extensions.md` - Cursor IDE CLI reference
- `gemini_cli_extensions.md` - Gemini CLI reference
- `kiro_cli_extensions.md` - Kiro (AWS) CLI reference
- `vibe_cli_extensions.md` - Vibe (Mistral) CLI reference
- `comparatif_cli_ia.md` - Comparison of AI CLIs

User guides:
- `README.md` - Main user documentation
- `GUIDE_INSTALLATION_FASTER_WHISPER.md` - Faster-Whisper setup
- `GUIDE_DEMARRAGE_AUTOMATIQUE.md` - Windows service setup
