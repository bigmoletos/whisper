@echo off
REM Installs all the necessary dependencies for the project, including pytest and pyinstaller.

echo "Installing dependencies..."
call ..\venv_whisper\Scripts\activate.bat
pip install -r ..\requirements.txt
pip install pytest
pip install pyinstaller
echo "Done."
pause
