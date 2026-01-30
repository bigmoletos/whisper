@echo off
chcp 65001 >nul

echo ================================================
echo    VOICE-TO-TEXT TURBO - MODE FALLBACK
echo    (Whisper standard au lieu de Faster-Whisper)
echo ================================================
echo.

:: Répertoires
set "PROJECT_DIR=%~dp0"
set "ROOT_DIR=%PROJECT_DIR%..\.."
set "SHARED_DIR=%ROOT_DIR%\shared"

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé
    pause
    exit /b 1
)
echo [OK] Python 3.12 détecté

:: Vérifier les dépendances de base (sans Faster-Whisper)
echo [INFO] Vérification des dépendances de base...
py -3.12 -c "
try:
    import torch
    import whisper
    import sounddevice
    import pyautogui
    print('[OK] Dépendances de base disponibles')
except ImportError as e:
    print('[ERREUR] Dépendance manquante:', e)
    exit(1)
" >nul 2>&1

if errorlevel 1 (
    echo [WARNING] Dépendances manquantes - installation...
    py -3.12 -m pip install --user torch sounddevice pyautogui keyboard pyperclip openai-whisper
)

:: Vérifier main.py
if not exist "%SHARED_DIR%\src\main.py" (
    echo [ERREUR] main.py non trouvé
    pause
    exit /b 1
)

:: Lancement avec configuration fallback
echo.
echo [INFO] Démarrage en mode fallback (Whisper standard)...
echo [INFO] Raccourci: Ctrl+Alt+7 (toggle enregistrement)
echo [INFO] Logs: voice_transcriber_fallback.log
echo.

cd /d "%SHARED_DIR%\src"
py -3.12 main.py --config "%PROJECT_DIR%config_fallback.json"

echo.
if errorlevel 1 (
    echo [ERREUR] Échec du lancement
    echo [INFO] Vérifiez voice_transcriber_fallback.log
) else (
    echo [INFO] Application fermée normalement
)
pause