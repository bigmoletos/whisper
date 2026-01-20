@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ================================================
echo    MEETING TRANSCRIBER PRO - Assistant Avancé
echo    (Diarisation Pyannote + GPU)
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

:: Vérifier le token Hugging Face
if not defined TOKEN_HF (
    echo [AVERTISSEMENT] Variable TOKEN_HF non définie
    echo [INFO] La diarisation pyannote nécessite un token Hugging Face
    echo [INFO] Créez un token sur: https://huggingface.co/settings/tokens
    echo [INFO] Puis: set TOKEN_HF=votre_token
    echo.
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

:: Vérifier CUDA
where nvcc >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] CUDA non détecté. Performances réduites.
) else (
    echo [INFO] CUDA détecté - Accélération GPU activée
)

:: Vérifier Ollama
echo [INFO] Vérification d'Ollama pour les résumés...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] Ollama non détecté. Les résumés automatiques seront désactivés.
) else (
    echo [INFO] Ollama détecté - Résumés automatiques activés
)

:: Vérifier pyannote
python -c "import pyannote.audio" >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] pyannote-audio non installé
    echo [INFO] Installation: pip install pyannote.audio
) else (
    echo [INFO] pyannote-audio détecté - Diarisation avancée activée
)

:: Lancer l'application
echo.
echo [INFO] Démarrage de Meeting Transcriber Pro...
echo [INFO] Commandes: start (démarrer) / stop (arrêter) / status / quit
echo [INFO] Fonctionnalités: Diarisation avancée, GPU, Résumés IA
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
