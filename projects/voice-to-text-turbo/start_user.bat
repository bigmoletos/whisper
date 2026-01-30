@echo off
chcp 65001 >nul

echo ================================================
echo    VOICE-TO-TEXT TURBO - Mode User Python 3.12
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
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    exit /b 1
)
echo [OK] Python 3.12 détecté

:: Vérifier CUDA
echo [INFO] Vérification CUDA...
py -3.12 -c "import torch; print('[INFO] CUDA:', 'Disponible' if torch.cuda.is_available() else 'Non disponible')" 2>nul

:: Vérifier les dépendances critiques
echo [INFO] Vérification des dépendances...
py -3.12 -c "import faster_whisper, sounddevice, pyautogui" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Dépendances manquantes détectées
    echo [INFO] Lancez fix_turbo_user.bat pour les installer
    set /p choice="Continuer quand même ? (o/N) : "
    if /i not "%choice%"=="o" exit /b 1
)

:: Configuration
echo [INFO] Configuration Voice-to-Text Turbo...
if exist "%PROJECT_DIR%config.json" (
    echo [OK] Configuration trouvée
) else (
    echo [WARNING] Configuration non trouvée, utilisation des paramètres par défaut
)

:: Vérifier main.py
if not exist "%SHARED_DIR%\src\main.py" (
    echo [ERREUR] Fichier main.py non trouvé: %SHARED_DIR%\src\main.py
    pause
    exit /b 1
)

:: Lancement
echo.
echo [INFO] Démarrage de Voice-to-Text Turbo...
echo [INFO] Raccourci: Ctrl+Alt+7 (toggle enregistrement)
echo [INFO] Appuyez sur Ctrl+C pour arrêter
echo.

cd /d "%SHARED_DIR%\src"
py -3.12 main.py --config "%PROJECT_DIR%config.json"

echo.
if errorlevel 1 (
    echo [ERREUR] L'application s'est terminée avec une erreur
    echo [INFO] Vérifiez les messages ci-dessus
) else (
    echo [INFO] Application fermée normalement
)
pause