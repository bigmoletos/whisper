@echo off
chcp 65001 >nul

echo ================================================
echo    DIAGNOSTIC VOICE-TO-TEXT TURBO
echo ================================================
echo.

:: Test Python 3.12
echo [1] Test Python 3.12...
py -3.12 --version
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé
    pause
    exit /b 1
)
echo [OK] Python 3.12 disponible
echo.

:: Test imports critiques
echo [2] Test des imports critiques...
py -3.12 -c "
try:
    import sys
    print('Python version:', sys.version)
    
    import torch
    print('PyTorch:', torch.__version__)
    print('CUDA disponible:', torch.cuda.is_available())
    
    import faster_whisper
    print('Faster-Whisper: OK')
    
    import sounddevice
    print('SoundDevice: OK')
    
    print('=== TOUS LES IMPORTS OK ===')
except ImportError as e:
    print('ERREUR IMPORT:', e)
    exit(1)
except Exception as e:
    print('ERREUR:', e)
    exit(1)
"
if errorlevel 1 (
    echo [ERREUR] Problème avec les imports
    pause
    exit /b 1
)
echo.

:: Test fichier main.py
echo [3] Test fichier main.py...
if not exist "shared\src\main.py" (
    echo [ERREUR] main.py non trouvé
    pause
    exit /b 1
)
echo [OK] main.py trouvé
echo.

:: Test configuration
echo [4] Test configuration...
if not exist "projects\voice-to-text-turbo\config.json" (
    echo [ERREUR] config.json non trouvé
    pause
    exit /b 1
)
echo [OK] config.json trouvé
echo.

:: Test lancement avec timeout
echo [5] Test lancement (10 secondes max)...
echo [INFO] Lancement de Voice-to-Text Turbo...
echo [INFO] Le programme va se lancer pendant 10 secondes puis s'arrêter
echo.

timeout /t 3 >nul
py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json &
set PID=%!

timeout /t 10 >nul
taskkill /f /pid %PID% 2>nul

echo.
echo [INFO] Test terminé
echo.
pause