@echo off
REM Formats the code using black.

echo "Formatting code..."
call ..\venv_whisper\Scripts\activate.bat
pip install black
black ..\src
echo "Done."
pause
