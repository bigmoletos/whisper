@echo off
chcp 65001 >nul

echo ================================================
echo    RÉPARATION VOICE-TO-TEXT TURBO (MODE USER)
echo ================================================
echo.

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 requis
    pause
    exit /b 1
)
echo [OK] Python 3.12 détecté
echo.

:: Mise à jour pip
echo [INFO] Mise à jour de pip...
py -3.12 -m pip install --user --upgrade pip

:: Installation PyTorch avec CUDA (mode user)
echo [INFO] Installation PyTorch avec CUDA (mode user)...
py -3.12 -m pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

:: Installation Faster-Whisper
echo [INFO] Installation Faster-Whisper...
py -3.12 -m pip install --user faster-whisper

:: Installation dépendances audio
echo [INFO] Installation dépendances audio...
py -3.12 -m pip install --user sounddevice numpy scipy

:: Installation dépendances système Windows
echo [INFO] Installation dépendances système...
py -3.12 -m pip install --user pyautogui keyboard pyperclip pywin32

:: Installation Whisper standard (fallback)
echo [INFO] Installation Whisper standard...
py -3.12 -m pip install --user openai-whisper

:: Test final
echo.
echo [INFO] Test de l'installation...
py -3.12 -c "
import sys
import torch
import faster_whisper
import sounddevice
import pyautogui

print('=== TEST INSTALLATION ===')
print('Python:', sys.version.split()[0])
print('PyTorch:', torch.__version__)
print('CUDA disponible:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU:', torch.cuda.get_device_name(0))
print('Faster-Whisper: OK')
print('SoundDevice: OK')
print('PyAutoGUI: OK')
print('=== INSTALLATION RÉUSSIE ===')
"

if errorlevel 1 (
    echo [ERREUR] Test d'installation échoué
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Réparation terminée !
echo [INFO] Vous pouvez maintenant tester Voice-to-Text Turbo
echo.
pause