@echo off
chcp 65001 >nul

echo ================================================
echo    VOICE-TO-TEXT TURBO - Version Simplifiée
echo    (Faster-Whisper - GPU/CUDA)
echo ================================================
echo.

:: Répertoire du projet
set "PROJECT_DIR=%~dp0"
set "ROOT_DIR=%PROJECT_DIR%..\.."
set "SHARED_DIR=%ROOT_DIR%\shared"
set "VENV_DIR=%ROOT_DIR%\venv_whisper"

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé. Versions disponibles :
    py -0 2>nul
    echo [INFO] Appuyez sur une touche pour fermer...
    pause >nul
    exit /b 1
)
echo [OK] Python 3.12 détecté

:: Vérifier l'environnement virtuel
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Environnement virtuel non trouvé, création avec Python 3.12...
    py -3.12 -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERREUR] Échec de création de l'environnement virtuel
        echo [INFO] Appuyez sur une touche pour fermer...
        pause >nul
        exit /b 1
    )
    echo [OK] Environnement virtuel créé
)

:: Activation de l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call "%VENV_DIR%\Scripts\activate.bat" 2>nul
if errorlevel 1 (
    echo [ERREUR] Échec de l'activation de l'environnement virtuel
    echo [INFO] Recréation de l'environnement...
    rmdir /s /q "%VENV_DIR%" 2>nul
    py -3.12 -m venv "%VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
)

:: Vérifier que Python fonctionne dans le venv
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non fonctionnel dans l'environnement virtuel
    echo [INFO] Appuyez sur une touche pour fermer...
    pause >nul
    exit /b 1
)

echo [OK] Environnement virtuel activé

:: Configuration du projet
echo [INFO] Configuration du projet Voice-to-Text Turbo...
if exist "%PROJECT_DIR%config.json" (
    if not exist "%SHARED_DIR%\src" mkdir "%SHARED_DIR%\src" 2>nul
    copy "%PROJECT_DIR%config.json" "%SHARED_DIR%\src\config.json" >nul 2>&1
    if exist "%SHARED_DIR%\src\config.json" (
        echo [OK] Configuration Turbo activée
    ) else (
        echo [WARNING] Échec de copie de configuration, utilisation des paramètres par défaut
    )
) else (
    echo [WARNING] Fichier config.json non trouvé dans le projet
)

:: Vérifier que le répertoire source existe
if not exist "%SHARED_DIR%\src\main.py" (
    echo [ERREUR] Fichier main.py non trouvé: %SHARED_DIR%\src\main.py
    echo [INFO] Vérifiez l'installation du projet
    echo [INFO] Appuyez sur une touche pour fermer...
    pause >nul
    exit /b 1
)

:: Lancer l'application
echo.
echo [INFO] Démarrage de Voice-to-Text Turbo...
echo [INFO] Raccourci: Ctrl+Alt+7 (toggle enregistrement)
echo [INFO] CUDA sera détecté automatiquement par l'application
echo.

cd /d "%SHARED_DIR%\src"
echo [DEBUG] Répertoire de travail: %CD%
echo [DEBUG] Commande: python main.py --config "%PROJECT_DIR%config.json"
echo.

python main.py --config "%PROJECT_DIR%config.json"
set EXIT_CODE=%errorlevel%

if %EXIT_CODE% neq 0 (
    echo.
    echo [ERREUR] L'application s'est terminée avec une erreur (code: %EXIT_CODE%)
    echo [INFO] Vérifiez les messages d'erreur ci-dessus
    echo [INFO] Appuyez sur une touche pour fermer...
    pause >nul
) else (
    echo.
    echo [INFO] Application fermée normalement
)