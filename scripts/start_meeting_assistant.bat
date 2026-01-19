@echo off
REM =======================================================
REM Meeting Assistant - Script de lancement
REM =======================================================

setlocal enabledelayedexpansion

REM Aller dans le répertoire du script
cd /d "%~dp0\.."

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

REM Vérifier l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] Pas d'environnement virtuel détecté, utilisation de Python système
)

REM Paramètres
set MEETING_NAME=%~1
if "%MEETING_NAME%"=="" set MEETING_NAME=Réunion

REM Lancer Meeting Assistant
echo.
echo =======================================================
echo   Meeting Assistant
echo =======================================================
echo.
echo   Démarrage de la session: %MEETING_NAME%
echo.

python -m meeting_assistant start --name "%MEETING_NAME%"

REM Pause si erreur
if errorlevel 1 (
    echo.
    echo [ERREUR] Une erreur s'est produite
    pause
)

endlocal
