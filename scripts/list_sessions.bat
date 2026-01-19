@echo off
REM =======================================================
REM Meeting Assistant - Liste des sessions
REM =======================================================

cd /d "%~dp0\.."

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

python -m meeting_assistant list

pause
