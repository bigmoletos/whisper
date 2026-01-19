@echo off
REM Checks the code for type errors using mypy.

echo "Checking code for type errors..."
call ..\venv_whisper\Scripts\activate.bat
pip install mypy
mypy ..\src
echo "Done."
pause
