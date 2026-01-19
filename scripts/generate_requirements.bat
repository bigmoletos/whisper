@echo off
REM Generates a requirements.txt file with the exact versions of the dependencies.

echo "Generating requirements.txt..."
call ..\venv_whisper\Scripts\activate.bat
pip freeze > ..\requirements.txt
echo "Done."
pause
