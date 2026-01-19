@echo off
REM Checks for updates to the dependencies and updates them if necessary.

echo "Checking for updates..."
call ..\venv_whisper\Scripts\activate.bat
pip list --outdated
echo "Updating dependencies..."
pip install --upgrade -r ..\requirements.txt
echo "Done."
pause
