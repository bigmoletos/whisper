@echo off
echo ========================================
echo   INSTALLATION VTT AVEC PIPX
echo ========================================
echo.

cd /d "%~dp0\.."

echo [INFO] Verification de pipx...
where pipx >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de pipx...
    python -m pip install --user pipx
    python -m pipx ensurepath
    echo [INFO] Redemarrez votre terminal apres cette installation
    pause
    exit /b 1
)

echo [INFO] pipx detecte
pipx --version

echo [INFO] Installation des outils VTT avec pipx...

REM Installation des packages principaux
echo [INFO] Installation de openai-whisper...
pipx install openai-whisper

echo [INFO] Installation de faster-whisper...
pipx install faster-whisper

echo [INFO] Injection des dependances CUDA dans l'environnement whisper...
pipx inject openai-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo [INFO] Injection des dependances audio...
pipx inject openai-whisper sounddevice pyaudio numpy scipy

echo [INFO] Injection des dependances systeme...
pipx inject openai-whisper pyautogui pywin32 keyboard pyperclip python-dotenv

echo [INFO] Test de l'installation...
pipx run whisper --help >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Installation echouee
    pause
    exit /b 1
)

echo [INFO] Test CUDA...
pipx run python -c "
import torch
print('CUDA disponible:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU:', torch.cuda.get_device_name(0))
"

echo.
echo [SUCCESS] Installation pipx terminee avec succes
echo.
echo PROCHAINES ETAPES:
echo 1. Redemarrez votre terminal
echo 2. Testez: pipx run whisper --help
echo 3. Lancez VTT normalement
echo.
pause