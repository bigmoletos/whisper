@echo off
REM Checks the code for style errors using flake8.

echo "Checking code for style errors..."
call ..\venv_whisper\Scripts\activate.bat
pip install flake8
flake8 ..\src
echo "Done."
pause
