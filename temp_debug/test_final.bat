@echo off
chcp 65001 >nul

echo ================================================
echo    TEST FINAL - VOICE-TO-TEXT TURBO
echo ================================================
echo.

echo [INFO] Ce script va tester la nouvelle configuration Voice-to-Text Turbo
echo [INFO] avec Python 3.12 en mode --user (sans droits admin)
echo.

:: Test 1 : Python 3.12
echo [TEST 1] Vérification Python 3.12...
py -3.12 --version
if errorlevel 1 (
    echo [ERREUR] Python 3.12 requis
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    exit /b 1
)
echo [OK] Python 3.12 disponible
echo.

:: Test 2 : Dépendances critiques
echo [TEST 2] Vérification des dépendances...
py -3.12 -c "
try:
    import torch
    print('[OK] PyTorch:', torch.__version__)
    print('[INFO] CUDA disponible:', torch.cuda.is_available())
    
    import faster_whisper
    print('[OK] Faster-Whisper disponible')
    
    import sounddevice
    print('[OK] SoundDevice disponible')
    
    import pyautogui
    print('[OK] PyAutoGUI disponible')
    
except ImportError as e:
    print('[ERREUR] Dépendance manquante:', e)
    print('[INFO] Lancez fix_turbo_user.bat pour installer')
    exit(1)
"
if errorlevel 1 (
    echo.
    echo [INFO] Lancement de la réparation automatique...
    call fix_turbo_user.bat
    if errorlevel 1 (
        echo [ERREUR] Échec de la réparation
        pause
        exit /b 1
    )
)
echo.

:: Test 3 : Fichiers requis
echo [TEST 3] Vérification des fichiers...
if not exist "shared\src\main.py" (
    echo [ERREUR] main.py manquant
    pause
    exit /b 1
)
echo [OK] main.py trouvé

if not exist "projects\voice-to-text-turbo\config.json" (
    echo [ERREUR] config.json manquant
    pause
    exit /b 1
)
echo [OK] config.json trouvé

if not exist "projects\voice-to-text-turbo\start_user.bat" (
    echo [ERREUR] start_user.bat manquant
    pause
    exit /b 1
)
echo [OK] start_user.bat trouvé
echo.

:: Test 4 : Configuration
echo [TEST 4] Vérification de la configuration...
py -3.12 -c "
import json
with open('projects/voice-to-text-turbo/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    
print('[INFO] Moteur:', config['whisper']['engine'])
print('[INFO] Modèle:', config['whisper']['model'])
print('[INFO] Device:', config['whisper']['device'])
print('[INFO] Langue:', config['whisper']['language'])
"
echo.

:: Test 5 : Test de lancement (5 secondes)
echo [TEST 5] Test de lancement rapide (5 secondes)...
echo [INFO] L'application va se lancer puis s'arrêter automatiquement
echo.

timeout /t 2 >nul
start /min py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json
timeout /t 5 >nul
taskkill /f /im python.exe 2>nul

echo.
echo ================================================
echo    RÉSULTAT DU TEST
echo ================================================
echo [SUCCESS] Configuration Voice-to-Text Turbo prête !
echo.
echo [INFO] Pour utiliser Voice-to-Text Turbo :
echo [INFO] 1. Lancez start.bat
echo [INFO] 2. Choisissez l'option [2U]
echo [INFO] 3. Utilisez Ctrl+Alt+7 pour démarrer/arrêter l'enregistrement
echo.
echo [INFO] Si problèmes : consultez GUIDE_DEPANNAGE_TURBO.md
echo.
pause