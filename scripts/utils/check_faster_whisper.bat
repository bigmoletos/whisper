@echo off
REM Checks if faster-whisper is configured and if Rust is installed.

REM Check if config.json exists
if not exist ..\config.json (
    echo "config.json not found."
    exit /b 1
)

REM Check if faster-whisper is configured
findstr /C:"\"engine\": \"faster-whisper\"" ..\config.json >nul
if %errorlevel% equ 0 (
    REM faster-whisper is configured, check for Rust
    rustc --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo "WARNING: faster-whisper is configured in config.json, but Rust is not installed."
        echo "The application will fall back to the standard whisper engine."
        echo "To use faster-whisper, please install Rust from https://rustup.rs/"
        pause
    )
)

