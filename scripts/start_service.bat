@echo off
REM Script de demarrage du service Whisper STT Global
REM Auteur: Bigmoletos
REM Date: 2025-01-11

echo ========================================
echo Demarrage de Whisper STT Global
echo ========================================
echo.

REM Changer vers le répertoire du projet
cd /d "%~dp0.."

REM Vérifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Vérifier que les dépendances sont installées
python -c "import whisper; import sounddevice; import pyautogui; import keyboard" >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Les dependances ne sont pas installees
    echo Veuillez executer scripts\install.bat d'abord
    pause
    exit /b 1
)

REM Lancer le service
echo Demarrage du service...
echo Appuyez sur Ctrl+C pour arreter
echo.

REM Ajouter le répertoire parent au PYTHONPATH pour les imports
set PYTHONPATH=%CD%;%PYTHONPATH%
python -m src.main

pause
