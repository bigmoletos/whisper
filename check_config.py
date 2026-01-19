# -*- coding: utf-8 -*-
"""
Script to check the configuration file (config.json) for the Whisper STT Global application.
"""

import json
from pathlib import Path

def check_config():
    """
    Checks the config.json file for correct configuration.
    """
    config_path = Path("config.json")
    if not config_path.exists():
        print(f"ERROR: Configuration file not found at {config_path.resolve()}")
        return False

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON in {config_path.resolve()}")
        return False

    errors = []

    # Check whisper section
    whisper_config = config.get("whisper", {})
    if not whisper_config:
        errors.append("`whisper` section is missing in config.json")
    else:
        if whisper_config.get("engine") not in ["whisper", "faster-whisper", "whisper-cpp"]:
            errors.append(f"Invalid whisper engine: {whisper_config.get('engine')}. Must be one of: whisper, faster-whisper, whisper-cpp")
        if whisper_config.get("model") not in ["tiny", "base", "small", "medium", "large"]:
            errors.append(f"Invalid whisper model: {whisper_config.get('model')}. Must be one of: tiny, base, small, medium, large")
        if whisper_config.get("device") not in ["cpu", "cuda"]:
            errors.append(f"Invalid whisper device: {whisper_config.get('device')}. Must be 'cpu' or 'cuda'")
        if whisper_config.get("compute_type") not in ["int8", "float16", "float32"]:
            errors.append(f"Invalid whisper compute_type: {whisper_config.get('compute_type')}. Must be one of: int8, float16, float32")
        if whisper_config.get("language") not in ["en", "fr", "es", "de", "it"]:
            errors.append(f"Invalid or unsupported language: {whisper_config.get('language')}. Supported languages are: en, fr, es, de, it")

    # Check hotkey section
    hotkey_config = config.get("hotkey", {})
    if not hotkey_config:
        errors.append("`hotkey` section is missing in config.json")
    else:
        if not hotkey_config.get("modifiers"):
            errors.append("`modifiers` are missing in the `hotkey` section")
        if not hotkey_config.get("key"):
            errors.append("`key` is missing in the `hotkey` section")

    # Check logging section
    logging_config = config.get("logging", {})
    if not logging_config:
        errors.append("`logging` section is missing in config.json")
    else:
        if logging_config.get("level") not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            errors.append(f"Invalid logging level: {logging_config.get('level')}. Must be one of: DEBUG, INFO, WARNING, ERROR")

    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"- {error}")
        return False

    print("Configuration seems OK.")
    return True

if __name__ == "__main__":
    if not check_config():
        exit(1)
