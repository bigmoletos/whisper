@echo off
chcp 65001 >nul 2>&1
setlocal

REM =======================================================
REM   BOT ASSISTANT DE RÉUNION - Démarrage ULTRA RAPIDE
REM   Double-cliquez et c'est parti !
REM =======================================================

title Bot Assistant de Réunion - Enregistrement

cd /d "%~dp0"

REM Activer l'environnement virtuel si présent
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Générer un nom avec date/heure
for /f "tokens=1-3 delims=/" %%a in ('date /t') do set DATESTAMP=%%c-%%b-%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIMESTAMP=%%a-%%b
set MEETING_NAME=Reunion_%DATESTAMP%_%TIMESTAMP%

cls
echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║      BOT ASSISTANT DE RÉUNION - ENREGISTREMENT            ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.
echo   Session: %MEETING_NAME%
echo.
echo   Commandes:  p=Pause  s=Status  q=Arreter
echo.
echo  ═══════════════════════════════════════════════════════════
echo.

python -m meeting_assistant start --name "%MEETING_NAME%"

echo.
pause
endlocal
