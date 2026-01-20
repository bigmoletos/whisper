@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ================================================
echo    MEETING TRANSCRIBER - Assistant de Réunion
echo    (Transcription + Résumé Automatique)
echo ================================================
echo.

:: Répertoire du projet
set "PROJECT_DIR=%~dp0"
set "ROOT_DIR=%PROJECT_DIR%..\.."
set "SHARED_DIR=%ROOT_DIR%\shared"
set "VENV_DIR=%ROOT_DIR%\venv_whisper"
set "MEETING_LIB=%SHARED_DIR%\lib\meeting_assistant"

:: Créer les répertoires de sortie
if not exist "%PROJECT_DIR%sessions" mkdir "%PROJECT_DIR%sessions"
if not exist "%PROJECT_DIR%reports" mkdir "%PROJECT_DIR%reports"

:: Vérifier Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non trouvé. Veuillez installer Python 3.10+
    pause
    exit /b 1
)

:: Vérifier et créer/réparer l'environnement virtuel
if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Activation de l'environnement virtuel...
    call "%VENV_DIR%\Scripts\activate.bat"

    :: Vérifier si pip fonctionne
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo [AVERTISSEMENT] Environnement virtuel corrompu détecté
        echo [INFO] Suppression et recréation de l'environnement virtuel...
        call deactivate 2>nul
        rmdir /s /q "%VENV_DIR%"
        python -m venv "%VENV_DIR%"
        call "%VENV_DIR%\Scripts\activate.bat"
    )
) else (
    echo [AVERTISSEMENT] Environnement virtuel non trouvé
    echo [INFO] Création de l'environnement virtuel...
    python -m venv "%VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
)

:: Vérifier si les dépendances sont installées
python -c "import sounddevice, whisper" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dépendances requises...
    python -m pip install --upgrade pip
    python -m pip install -r "%ROOT_DIR%\requirements.txt"
    if errorlevel 1 (
        echo [ERREUR] Échec de l'installation des dépendances
        pause
        exit /b 1
    )
    echo [OK] Dépendances installées avec succès
)

:: Vérifier Ollama (pour les résumés)
echo [INFO] Vérification d'Ollama pour les résumés...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] Ollama non détecté. Les résumés automatiques seront désactivés.
    echo [INFO] Pour activer les résumés, installez Ollama: https://ollama.ai
) else (
    echo [INFO] Ollama détecté - Résumés automatiques activés
)

:: Lancer l'application
echo.
echo [INFO] Démarrage de Meeting Transcriber...
echo [INFO] Commandes: start (démarrer) / stop (arrêter) / status / quit
echo.

set "PYTHONPATH=%SHARED_DIR%\lib;%SHARED_DIR%\src;%PYTHONPATH%"
cd /d "%PROJECT_DIR%"
python -m meeting_assistant --config "%PROJECT_DIR%config.json"

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est terminée avec une erreur
    pause
)

endlocal
