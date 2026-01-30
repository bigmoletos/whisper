@echo off
chcp 65001 >nul

echo ================================================
echo    TEST MODULES PYTHON
echo ================================================
echo.

echo [INFO] Vérification des modules Python requis...
echo.

py -3.12 -c "import sys; print('Python version:', sys.version); print('Python executable:', sys.executable)"

echo.
echo [INFO] Test des modules individuels...

py -3.12 -c "import json; print('[OK] json')" 2>nul || echo [MANQUANT] json
py -3.12 -c "import logging; print('[OK] logging')" 2>nul || echo [MANQUANT] logging
py -3.12 -c "import pathlib; print('[OK] pathlib')" 2>nul || echo [MANQUANT] pathlib
py -3.12 -c "import numpy; print('[OK] numpy')" 2>nul || echo [MANQUANT] numpy
py -3.12 -c "import sounddevice; print('[OK] sounddevice')" 2>nul || echo [MANQUANT] sounddevice
py -3.12 -c "import torch; print('[OK] torch')" 2>nul || echo [MANQUANT] torch
py -3.12 -c "import faster_whisper; print('[OK] faster_whisper')" 2>nul || echo [MANQUANT] faster_whisper
py -3.12 -c "import pyautogui; print('[OK] pyautogui')" 2>nul || echo [MANQUANT] pyautogui
py -3.12 -c "import keyboard; print('[OK] keyboard')" 2>nul || echo [MANQUANT] keyboard
py -3.12 -c "import pyperclip; print('[OK] pyperclip')" 2>nul || echo [MANQUANT] pyperclip

echo.
pause