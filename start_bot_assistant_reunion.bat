@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM =======================================================
REM   BOT ASSISTANT DE RÉUNION - Lancement Rapide
REM =======================================================

title Bot Assistant de Réunion

cd /d "%~dp0"

cls
echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║                                                           ║
echo  ║          BOT ASSISTANT DE RÉUNION TEAMS                   ║
echo  ║                                                           ║
echo  ║   Transcription automatique + Résumé intelligent          ║
echo  ║                                                           ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    pause
    exit /b 1
)

REM Activer l'environnement virtuel si présent
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Demander le nom de la réunion
echo  Entrez le nom de la reunion (ou appuyez sur Entree pour "Reunion") :
echo.
set /p MEETING_NAME="  Nom: "

if "%MEETING_NAME%"=="" set MEETING_NAME=Reunion

echo.
echo  ───────────────────────────────────────────────────────────
echo   Demarrage de: %MEETING_NAME%
echo  ───────────────────────────────────────────────────────────
echo.
echo   Commandes pendant l'enregistrement:
echo     p - Pause / Reprendre
echo     s - Voir le status
echo     q - Arreter et generer le rapport
echo.
echo  ───────────────────────────────────────────────────────────
echo.

REM Lancer le bot
python -m meeting_assistant start --name "%MEETING_NAME%"

echo.
echo  ───────────────────────────────────────────────────────────
echo   Session terminee
echo  ───────────────────────────────────────────────────────────
echo.

pause
endlocal
