@echo off
REM =======================================================
REM Meeting Assistant - Installation des dépendances
REM =======================================================

setlocal enabledelayedexpansion

echo.
echo =======================================================
echo   Meeting Assistant - Installation
echo =======================================================
echo.

REM Aller dans le répertoire du script
cd /d "%~dp0\.."

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python 3.10+ depuis https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYVER=%%a
echo [OK] Python %PYVER% détecté

REM Vérifier/Créer l'environnement virtuel
if not exist "venv" (
    echo.
    echo Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Échec création environnement virtuel
        pause
        exit /b 1
    )
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre à jour pip
echo.
echo Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances principales
echo.
echo Installation des dépendances principales...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [AVERTISSEMENT] Certaines dépendances principales ont échoué
    )
)

REM Installer les dépendances Meeting Assistant
echo.
echo Installation des dépendances Meeting Assistant...
if exist "requirements_meeting.txt" (
    pip install -r requirements_meeting.txt
    if errorlevel 1 (
        echo [AVERTISSEMENT] Certaines dépendances ont échoué
    )
)

REM Vérifier PyAudioWPatch
echo.
echo Vérification de PyAudioWPatch (capture audio système)...
python -c "import pyaudiowpatch" 2>nul
if errorlevel 1 (
    echo [INFO] Installation de PyAudioWPatch...
    pip install PyAudioWPatch
    if errorlevel 1 (
        echo [AVERTISSEMENT] PyAudioWPatch non installé - la capture audio système peut ne pas fonctionner
        echo Vous pouvez essayer: pip install pyaudio
    )
)

REM Vérifier faster-whisper
echo.
echo Vérification de faster-whisper...
python -c "from faster_whisper import WhisperModel" 2>nul
if errorlevel 1 (
    echo [INFO] faster-whisper non disponible, installation...
    pip install faster-whisper
    if errorlevel 1 (
        echo [AVERTISSEMENT] faster-whisper non installé
        echo Vous devrez peut-être installer Rust: https://rustup.rs/
    )
)

REM Créer les répertoires
echo.
echo Création des répertoires...
if not exist "meeting_reports" mkdir meeting_reports
if not exist "meeting_sessions" mkdir meeting_sessions

REM Vérifier Ollama
echo.
echo Vérification d'Ollama (LLM local)...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [INFO] Ollama n'est pas accessible sur localhost:11434
    echo.
    echo Pour utiliser l'analyse LLM locale:
    echo   1. Téléchargez Ollama: https://ollama.ai
    echo   2. Lancez: ollama run llama3.2
    echo.
    echo Sinon, configurez OPENAI_API_KEY ou ANTHROPIC_API_KEY dans les variables d'environnement
) else (
    echo [OK] Ollama accessible
)

echo.
echo =======================================================
echo   Installation terminée!
echo =======================================================
echo.
echo   Pour démarrer une réunion:
echo     scripts\start_meeting_assistant.bat "Nom de la réunion"
echo.
echo   Ou directement:
echo     python -m meeting_assistant start --name "Ma Réunion"
echo.
echo   Commandes disponibles:
echo     python -m meeting_assistant start --name "..."  - Démarrer
echo     python -m meeting_assistant list                - Lister les sessions
echo     python -m meeting_assistant status              - Status
echo.

pause
endlocal
