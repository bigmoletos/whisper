@echo off
echo ========================================
echo   ADAPTATION VOCALE - WHISPER STT
echo ========================================
echo.
echo Ce script va vous aider a ameliorer la reconnaissance
echo de votre voix pour les termes techniques.
echo.

cd /d "%~dp0\.."

echo [INFO] Activation de l'environnement virtuel...
if exist "venv_whisper\Scripts\activate.bat" (
    call venv_whisper\Scripts\activate.bat
) else (
    echo [ERREUR] Environnement virtuel non trouve
    echo Executez d'abord l'installation (option I du menu)
    pause
    exit /b 1
)

echo [INFO] Verification des dependances...
python -c "import pyaudio, whisper, numpy" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances manquantes...
    pip install pyaudio numpy openai-whisper
)

echo.
echo [INFO] Lancement de la session d'adaptation vocale...
echo.
python scripts\voice_adaptation.py

echo.
echo [INFO] Session d'adaptation terminee
pause