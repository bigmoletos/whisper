@echo off
REM Runs the application as a service.

echo "Running the application as a service..."
call ..\venv_whisper\Scripts\activate.bat
python ..\src\main.py --service
echo "Done."
pause
