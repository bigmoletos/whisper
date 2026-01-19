@echo off
REM Updates the requirements.txt file with the current environment.

echo "Updating requirements.txt..."
call ..\venv_whisper\Scripts\activate.bat
pip freeze > ..\requirements.txt
echo "Done."
pause
