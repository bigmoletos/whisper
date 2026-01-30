@echo off
echo ========================================
echo   INSTALLATION MODERNE VTT (PIPX)
echo   Python 3.12 + pipx
echo ========================================
echo.

cd /d "%~dp0\.."

REM Verification de Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé. Versions disponibles :
    py -0 2>nul
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    exit /b 1
)

echo [OK] Python 3.12 détecté

REM Installation/verification de pipx avec Python 3.12
echo [INFO] Verification de pipx...
pipx --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de pipx avec Python 3.12...
    py -3.12 -m pip install --user pipx
    py -3.12 -m pipx ensurepath
    
    REM Ajouter pipx au PATH pour cette session
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
    
    echo [INFO] pipx installé. Vérification...
    pipx --version >nul 2>&1
    if errorlevel 1 (
        echo [AVERTISSEMENT] Redémarrez votre terminal et relancez ce script
        echo [INFO] Ou ajoutez manuellement %USERPROFILE%\.local\bin au PATH
        pause
        exit /b 0
    )
)

echo [SUCCESS] pipx prêt

REM Configurer pipx pour utiliser Python 3.12 par défaut
echo [INFO] Configuration de pipx pour Python 3.12...
for /f "delims=" %%i in ('py -3.12 -c "import sys; print(sys.executable)"') do set "PYTHON312_PATH=%%i"
echo [DEBUG] Chemin Python 3.12: %PYTHON312_PATH%

REM Creation d'un environnement dedie pour VTT
echo [INFO] Creation de l'environnement VTT...
pipx install --force --python "%PYTHON312_PATH%" openai-whisper

REM Installation des dependances CUDA
echo [INFO] Installation PyTorch CUDA...
pipx inject openai-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

REM Installation faster-whisper
echo [INFO] Installation faster-whisper...
pipx inject openai-whisper faster-whisper

REM Dependances audio
echo [INFO] Installation dependances audio...
pipx inject openai-whisper sounddevice pyaudio numpy scipy

REM Dependances systeme Windows
echo [INFO] Installation dependances systeme...
pipx inject openai-whisper pyautogui keyboard pyperclip python-dotenv
pipx inject openai-whisper pywin32

REM Test final
echo [INFO] Test de l'installation...
pipx run --spec openai-whisper python -c "
import torch
import whisper
import faster_whisper
import sys
print('=== TEST INSTALLATION ===')
print('Python version:', sys.version)
print('Whisper: OK')
print('Faster-Whisper: OK')
print('PyTorch version:', torch.__version__)
print('CUDA disponible:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU:', torch.cuda.get_device_name(0))
print('=== INSTALLATION REUSSIE ===')
"

if errorlevel 1 (
    echo [ERREUR] Test d'installation echoue
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Installation moderne terminee avec succes
echo [INFO] Python 3.12 + pipx + CUDA configurés
echo.
echo UTILISATION:
echo - Whisper: pipx run --spec openai-whisper whisper audio.wav
echo - Python avec deps: pipx run --spec openai-whisper python script.py
echo.
echo PROCHAINES ETAPES:
echo 1. Utilisez l'option 2M du menu principal (Version Moderne)
echo 2. Testez la transcription
echo.
pause